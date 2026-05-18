"""
python manage.py activar_con_foto

Activa solo los productos que tienen foto asignada.
Desactiva todos los demas.
"""
from django.core.management.base import BaseCommand
from apps.productos.models import Producto


class Command(BaseCommand):
    help = "Activa productos con foto, desactiva los sin foto"

    def handle(self, *args, **options):
        # Activar los que tienen imagen
        activados = Producto.objects.exclude(
            imagen=""
        ).exclude(imagen=None).update(activo=True)

        # Desactivar los que NO tienen imagen
        desactivados = Producto.objects.filter(
            imagen=""
        ).update(activo=False)
        desactivados += Producto.objects.filter(
            imagen=None
        ).update(activo=False)

        self.stdout.write(self.style.SUCCESS(
            f"Activados: {activados}  |  Desactivados: {desactivados}"
        ))
