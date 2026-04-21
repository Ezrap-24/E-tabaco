from django.conf import settings
from django.db import models
import uuid


def generar_numero_orden():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


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
    total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=200, blank=True, db_index=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.numero_orden} — {self.cliente_nombre}"

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
