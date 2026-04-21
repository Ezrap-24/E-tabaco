from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import PerfilUsuario


@receiver(post_save, sender=User)
def crear_o_guardar_perfil_usuario(sender, instance, created, **kwargs):
    """Crea el perfil si es nuevo; lo guarda si ya existe."""
    if created:
        PerfilUsuario.objects.get_or_create(usuario=instance)
    else:
        # Solo guarda si el perfil ya existe en la BD (evita error si la migración no corrió)
        try:
            PerfilUsuario.objects.filter(usuario=instance).update()
            if hasattr(instance, 'perfil'):
                instance.perfil.save()
        except Exception:
            pass
