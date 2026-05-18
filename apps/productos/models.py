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
    INTENSIDAD_CHOICES = [
        ('Suave', 'Suave'),
        ('Medio', 'Medio'),
        ('Intenso', 'Intenso'),
    ]

    # Identificación
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=100, blank=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Clasificación
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )
    intensidad = models.CharField(
        max_length=10,
        choices=INTENSIDAD_CHOICES,
        blank=True
    )

    # Características físicas
    peso_gramos = models.IntegerField(blank=True, null=True)
    procedencia = models.CharField(max_length=100, blank=True)

    # Descripción e imagen
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='products/', blank=True, null=True)

    # Precios
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayor = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text='Precio por mayor (minimo cantidad_minima_mayor unidades)'
    )
    cantidad_minima_mayor = models.IntegerField(
        default=3,
        help_text='Cantidad minima para acceder al precio mayorista'
    )

    # Inventario
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(
        default=False,
        help_text='Marcar para mostrar en la sección de destacados del home'
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['marca', 'nombre']

    def __str__(self):
        return f'{self.marca} {self.nombre}' if self.marca else self.nombre

    def get_absolute_url(self):
        return reverse('productos:detalle', kwargs={'pk': self.pk})

    def tiene_stock(self):
        return self.stock > 0

    def precio_para(self, cantidad):
        """Retorna el precio unitario según la cantidad (mayorista o minorista)."""
        if self.precio_mayor and cantidad >= self.cantidad_minima_mayor:
            return self.precio_mayor
        return self.precio_unidad
