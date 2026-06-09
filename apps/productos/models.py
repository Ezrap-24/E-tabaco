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
    nombre = models.CharField(max_length=200, db_index=True)
    marca = models.CharField(max_length=100, blank=True, db_index=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Sección de navegación (Tabacos / Accesorios)
    seccion = models.CharField(max_length=50, blank=True,
                               help_text='Sección del nav: Tabacos, Accesorios, etc.')

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
    dimensiones = models.CharField(max_length=50, blank=True,
                                   help_text='Ej: 6x15 cm. Usar para accesorios en lugar de peso.')
    procedencia = models.CharField(max_length=100, blank=True)

    # Descripción e imágenes (principal + hasta 2 adicionales)
    descripcion = models.TextField(blank=True)
    imagen   = models.ImageField(upload_to='products/', blank=True, null=True)
    imagen_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    imagen_3 = models.ImageField(upload_to='products/', blank=True, null=True)

    # Precios
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for campo in ('imagen', 'imagen_2', 'imagen_3'):
            img_field = getattr(self, campo)
            if img_field:
                self._convertir_imagen_a_webp(campo, img_field)

    def _convertir_imagen_a_webp(self, campo, img_field):
        """Convierte una imagen a WebP, aplica sello y actualiza el campo."""
        import os
        from PIL import Image

        ruta = img_field.path
        if not os.path.exists(ruta) or ruta.lower().endswith('.webp'):
            # Ya es webp — solo aplicar sello si no lo tiene
            try:
                from apps.productos.watermark import aplicar_sello
                aplicar_sello(ruta)
            except Exception:
                pass
            return
        try:
            ruta_webp = os.path.splitext(ruta)[0] + '.webp'
            with Image.open(ruta) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    fondo = Image.new('RGBA', img.size, (255, 255, 255, 255))
                    fondo.paste(img.convert('RGBA'), mask=img.convert('RGBA').split()[3])
                    img = fondo.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((800, 800), Image.LANCZOS)
                img.save(ruta_webp, 'WEBP', quality=82, method=6)
            os.remove(ruta)
            nombre_webp = 'products/' + os.path.basename(ruta_webp)
            Producto.objects.filter(pk=self.pk).update(**{campo: nombre_webp})
            img_field.name = nombre_webp
            ruta_webp_final = ruta_webp
        except Exception:
            return

        try:
            from apps.productos.watermark import aplicar_sello
            aplicar_sello(ruta_webp_final)
        except Exception:
            pass

    def get_absolute_url(self):
        return reverse('productos:detalle', kwargs={'pk': self.pk})

    def tiene_stock(self):
        return self.stock > 0

