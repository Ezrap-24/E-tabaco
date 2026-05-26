from django.contrib.auth.models import User
from django.db import models


CATEGORIAS = [
    ('tabaco',      'Tabaco'),
    ('papelillos',  'Papelillos & Rolling'),
    ('filtros',     'Filtros & Tips'),
    ('accesorios',  'Accesorios'),
]


class SugerenciaProducto(models.Model):
    usuario    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sugerencia')
    categoria  = models.CharField(max_length=20, choices=CATEGORIAS)
    producto   = models.CharField(max_length=200)
    creado     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Sugerencia de producto'
        verbose_name_plural = 'Sugerencias de productos'
        ordering            = ['-creado']

    def __str__(self):
        return f'{self.usuario.username} — {self.get_categoria_display()}: {self.producto}'
