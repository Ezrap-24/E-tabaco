from django.db import models
import uuid


def generar_numero_orden():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


class Orden(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    numero_orden = models.CharField(max_length=20, unique=True, default=generar_numero_orden)
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20, blank=True)
    direccion_envio = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.numero_orden} — {self.cliente_nombre}"


class DetallePedido(models.Model):
    TIPOS = [('unidad', 'Unidad'), ('caja', 'Caja')]
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    tipo_venta = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} ({self.tipo_venta})"

    def subtotal(self):
        return self.precio_unitario * self.cantidad
