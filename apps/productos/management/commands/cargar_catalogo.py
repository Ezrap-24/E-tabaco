"""
Management command: cargar_catalogo
Carga el catalogo completo desde catalogo-111-PRODUCTOS.xlsx.
Copia fotos disponibles desde static/img/Fotos Productos/ a media/products/.

Uso:
    python manage.py cargar_catalogo
    python manage.py cargar_catalogo --limpiar      # borra productos existentes primero
    python manage.py cargar_catalogo --dry-run      # no guarda nada, solo muestra resumen
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.productos.models import Categoria, Producto


FOTO_DIRS = ['Tabacos', 'Accesorios']


def buscar_foto(nombre_archivo, base_fotos):
    """Busca la foto en las subcarpetas Tabacos/ y Accesorios/."""
    for subdir in FOTO_DIRS:
        ruta = base_fotos / subdir / nombre_archivo
        if ruta.exists():
            return ruta
    return None


class Command(BaseCommand):
    help = "Carga el catalogo desde catalogo-111-PRODUCTOS.xlsx"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Elimina todos los productos existentes antes de cargar",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Muestra lo que se haria sin guardar nada",
        )

    def handle(self, *args, **options):
        try:
            import openpyxl
        except ImportError:
            self.stderr.write(self.style.ERROR(
                "openpyxl no instalado. Ejecuta: pip install openpyxl"
            ))
            return

        dry_run = options["dry_run"]
        limpiar = options["limpiar"]

        base_dir = Path(settings.BASE_DIR)
        excel_path = base_dir / "catalogo-111-PRODUCTOS.xlsx"
        base_fotos = base_dir / "static" / "img" / "Fotos Productos"
        media_products = Path(settings.MEDIA_ROOT) / "products"

        if not excel_path.exists():
            self.stderr.write(self.style.ERROR(f"No se encontro: {excel_path}"))
            return

        if not dry_run:
            media_products.mkdir(parents=True, exist_ok=True)

        self.stdout.write("Leyendo catalogo-111-PRODUCTOS.xlsx ...")
        wb = openpyxl.load_workbook(str(excel_path))
        ws = wb.active

        headers = []
        for c in range(1, ws.max_column + 1):
            val = ws.cell(1, c).value
            if val:
                headers.append(val)
            else:
                break

        def col(row, field):
            try:
                idx = headers.index(field) + 1
                return ws.cell(row, idx).value
            except ValueError:
                return None

        if limpiar and not dry_run:
            n = Producto.objects.count()
            Producto.objects.all().delete()
            Categoria.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"Eliminados {n} productos y todas las categorias."
            ))

        prods_creados = 0
        prods_actualizados = 0
        fotos_copiadas = 0
        fotos_ya_existian = 0
        fotos_faltantes = 0
        fotos_sin_campo = 0

        for row in range(2, ws.max_row + 1):
            nombre = col(row, "nombre")
            if not nombre:
                continue

            categoria_nombre = col(row, "categoria") or "Sin categoria"
            marca = col(row, "marca") or ""
            codigo = col(row, "codigo") or None
            peso_gramos = col(row, "peso_gramos")
            procedencia = col(row, "procedencia") or ""
            intensidad = col(row, "intensidad") or ""
            descripcion = col(row, "descripcion") or ""
            precio_unidad = col(row, "precio_unidad") or 0
            precio_mayor = col(row, "precio_mayor")
            cantidad_minima_mayor = col(row, "cantidad_minima_mayor") or 3
            stock = col(row, "stock") or 0
            # activo solo si tiene foto disponible en disco
            activo = False  # se actualiza abajo si se encuentra la foto
            imagen_nombre = col(row, "imagen") or ""
            foto_disponible = str(col(row, "foto_disponible") or "NO").upper() == "SI"

            if intensidad not in ("Suave", "Medio", "Intenso"):
                intensidad = ""

            imagen_field = ""
            if foto_disponible and imagen_nombre:
                origen = buscar_foto(imagen_nombre, base_fotos)
                if origen:
                    destino = media_products / imagen_nombre
                    if not dry_run:
                        if not destino.exists():
                            shutil.copy2(str(origen), str(destino))
                            fotos_copiadas += 1
                        else:
                            fotos_ya_existian += 1
                    imagen_field = f"products/{imagen_nombre}"
                    activo = True  # tiene foto → se activa
                else:
                    fotos_faltantes += 1
                    self.stdout.write(
                        self.style.WARNING(f"  Foto no encontrada: {imagen_nombre} ({nombre})")
                    )
            else:
                fotos_sin_campo += 1

            if dry_run:
                if imagen_field:
                    prods_creados += 1
                else:
                    prods_creados += 1
                continue

            categoria, _ = Categoria.objects.get_or_create(
                nombre=categoria_nombre,
                defaults={"descripcion": ""},
            )

            defaults = {
                "nombre": nombre,
                "marca": marca,
                "categoria": categoria,
                "peso_gramos": peso_gramos,
                "procedencia": procedencia,
                "intensidad": intensidad,
                "descripcion": descripcion,
                "precio_unidad": precio_unidad,
                "precio_mayor": precio_mayor,
                "cantidad_minima_mayor": cantidad_minima_mayor,
                "stock": stock,
                "activo": activo,
                "destacado": False,
            }
            if imagen_field:
                defaults["imagen"] = imagen_field

            if codigo:
                prod, created = Producto.objects.update_or_create(
                    codigo=codigo,
                    defaults=defaults,
                )
            else:
                prod, created = Producto.objects.update_or_create(
                    nombre=nombre,
                    marca=marca,
                    defaults=defaults,
                )

            if created:
                prods_creados += 1
            else:
                prods_actualizados += 1

        self.stdout.write("")
        if dry_run:
            self.stdout.write(self.style.WARNING("--- DRY RUN (nada guardado) ---"))
            self.stdout.write(f"  Productos a cargar     : {prods_creados}")
            self.stdout.write(f"  Con foto en disco      : {prods_creados - fotos_faltantes - fotos_sin_campo}")
            self.stdout.write(f"  Sin foto (foto_disp=NO): {fotos_sin_campo}")
            self.stdout.write(f"  Foto marcada pero falta: {fotos_faltantes}")
        else:
            self.stdout.write(self.style.SUCCESS("--- Catalogo cargado ---"))
            self.stdout.write(f"  Creados              : {prods_creados}")
            self.stdout.write(f"  Actualizados         : {prods_actualizados}")
            self.stdout.write(f"  Fotos copiadas       : {fotos_copiadas}")
            self.stdout.write(f"  Fotos ya existian    : {fotos_ya_existian}")
            self.stdout.write(f"  Fotos no encontradas : {fotos_faltantes}")
            self.stdout.write(f"  Productos sin foto   : {fotos_sin_campo}")
            self.stdout.write("")
            self.stdout.write(
                "Ahora ve al Admin de Django y marca algunos productos como 'destacado'"
            )
            self.stdout.write("para que aparezcan en la seccion de inicio.")
