"""
Comando: aplicar_sello
Aplica el sello de agua "purotabaco.cl" a todas las imágenes en media/products/.

Uso:
    python manage.py aplicar_sello
    python manage.py aplicar_sello --dry-run    # muestra qué haría sin tocar nada
"""
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand


EXTENSIONES = {'.webp', '.jpg', '.jpeg', '.png'}


class Command(BaseCommand):
    help = 'Aplica sello de agua "purotabaco.cl" a todas las imágenes de productos.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', dest='dry_run',
                            help='Solo muestra las imágenes que se procesarían.')

    def handle(self, *args, **options):
        from apps.productos.watermark import aplicar_sello

        dry_run = options['dry_run']
        media_products = Path(settings.MEDIA_ROOT) / 'products'

        if not media_products.exists():
            self.stderr.write(self.style.ERROR(f'No existe: {media_products}'))
            return

        archivos = [f for f in sorted(media_products.iterdir())
                    if f.suffix.lower() in EXTENSIONES]

        if not archivos:
            self.stdout.write(self.style.WARNING('No se encontraron imágenes.'))
            return

        self.stdout.write(f'Imágenes encontradas: {len(archivos)}')
        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN] No se modificará nada.\n'))

        ok = errores = 0
        for archivo in archivos:
            if dry_run:
                self.stdout.write(f'  [dry] {archivo.name}')
                ok += 1
                continue
            try:
                aplicar_sello(str(archivo))
                self.stdout.write(f'  ✓ {archivo.name}')
                ok += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ {archivo.name}: {e}'))
                errores += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'{"[DRY RUN] " if dry_run else ""}Procesadas: {ok} | Errores: {errores}'
        ))
