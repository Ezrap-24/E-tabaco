from django.conf import settings
from django.db import models, transaction
import uuid


def generar_numero_orden():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


class ContadorOrden(models.Model):
    """Contador global para correlativos de órdenes pagadas.
    Siempre existe un único registro (pk=1). Se incrementa con select_for_update
    para garantizar unicidad incluso bajo carga concurrente.
    """
    ultimo = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Contador de órdenes'

    @classmethod
    def siguiente(cls):
        """Retorna el próximo correlativo de forma atómica."""
        with transaction.atomic():
            contador, _ = cls.objects.select_for_update().get_or_create(pk=1)
            contador.ultimo += 1
            contador.save(update_fields=['ultimo'])
            return contador.ultimo


class Orden(models.Model):
    ESTADOS = [
        ('pendiente_pago', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('preparando', 'Preparando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    numero_orden = models.CharField(max_length=20, unique=True, default=generar_numero_orden)

    # Correlativo secuencial asignado al confirmar el pago (PT-000001, PT-000002...)
    correlativo = models.PositiveIntegerField(null=True, blank=True, unique=True, db_index=True)

    # Relación con la cuenta del cliente (opcional: las compras como invitado son válidas).
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ordenes',
    )

    # Datos de contacto y envío (snapshot del momento de la compra).
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True)
    notas = models.TextField(blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente_pago')
    # Costo de despacho cobrado en el sitio (0 si se despacha por Starken "por
    # pagar" fuera de la RM). Incluido dentro de `total`.
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Mercado Pago (Checkout Pro): id de la preferencia creada y del pago aprobado.
    mp_preference_id = models.CharField(max_length=200, blank=True, db_index=True)
    mp_payment_id = models.CharField(max_length=200, blank=True, db_index=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.folio} — {self.cliente_nombre}"

    @property
    def folio(self):
        """Número de folio legible: PT-000001 si tiene correlativo, número_orden si no."""
        if self.correlativo:
            return f"PT-{self.correlativo:06d}"
        return self.numero_orden

    @property
    def codigo_barras(self):
        """Valor a codificar en el barcode (folio sin guión para mejor lectura)."""
        if self.correlativo:
            return f"PT{self.correlativo:06d}"
        return self.numero_orden

    @property
    def subtotal_productos(self):
        """Total de productos sin el despacho."""
        return self.total - self.costo_envio

    @property
    def direccion_envio(self):
        """Dirección formateada para mostrar en una sola línea."""
        partes = [self.direccion, self.ciudad, self.region]
        if self.codigo_postal:
            partes.append(self.codigo_postal)
        return ', '.join(p for p in partes if p)


class DetallePedido(models.Model):
    TIPOS = [('unidad', 'Unidad'), ('caja', 'Caja')]
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    # Snapshot del nombre por si el producto cambia o se borra.
    producto_nombre = models.CharField(max_length=200, blank=True)
    tipo_venta = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'

    def __str__(self):
        return f"{self.cantidad}x {self.producto_nombre or self.producto.nombre} ({self.tipo_venta})"

    def subtotal(self):
        return self.precio_unitario * self.cantidad
