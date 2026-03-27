from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_caja = models.DecimalField(max_digits=10, decimal_places=2)
    unidades_por_caja = models.IntegerField(default=10)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('productos:detalle', kwargs={'pk': self.pk})

    def tiene_stock(self):
        return self.stock > 0
