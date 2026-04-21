from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """Perfil extendido del usuario con datos de envío por defecto."""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"

    def tiene_direccion(self):
        return bool(self.direccion and self.ciudad)
