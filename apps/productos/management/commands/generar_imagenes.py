"""
Comando: python manage.py generar_imagenes
Genera imágenes genéricas de packaging para cada producto en la base de datos.
Requiere: Pillow (pip install pillow)
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from apps.productos.models import Producto

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False


# Paleta de colores e-Tabaco
PALETA = {
    'Tabaco Rubio':   {'fondo': (139, 105, 20),  'texto': (245, 240, 232)},   # dorado
    'Tabaco Negro':   {'fondo': (26, 26, 26),    'texto': (139, 105, 20)},    # negro + dorado
    'Tabaco Natural': {'fondo': (101, 78, 35),   'texto': (245, 240, 232)},   # marrón
}
COLOR_DEFAULT = {'fondo': (44, 44, 44), 'texto': (245, 240, 232)}


def crear_imagen_producto(nombre, categoria_nombre):
    """Crea una imagen de packaging simple para un producto."""
    W, H = 600, 600
    colores = PALETA.get(categoria_nombre, COLOR_DEFAULT)

    img = Image.new('RGB', (W, H), color=colores['fondo'])
    draw = ImageDraw.Draw(img)

    # Borde decorativo
    margen = 20
    draw.rectangle(
        [margen, margen, W - margen, H - margen],
        outline=colores['texto'],
        width=3
    )
    draw.rectangle(
        [margen + 8, margen + 8, W - margen - 8, H - margen - 8],
        outline=colores['texto'],
        width=1
    )

    # Línea superior decorativa
    draw.rectangle([margen + 15, margen + 15, W - margen - 15, margen + 60],
                   fill=colores['texto'])

    # Texto "e-Tabaco" en la franja superior
    try:
        font_brand = ImageFont.truetype("arial.ttf", 28)
        font_nombre = ImageFont.truetype("arial.ttf", 36)
        font_categoria = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font_brand = ImageFont.load_default()
        font_nombre = font_brand
        font_categoria = font_brand
        font_small = font_brand

    # "e-Tabaco" en franja superior
    draw.text((W // 2, margen + 37), "e-Tabaco",
              fill=colores['fondo'], font=font_brand, anchor="mm")

    # Categoría
    draw.text((W // 2, 160), categoria_nombre.upper(),
              fill=colores['texto'], font=font_categoria, anchor="mm")

    # Línea separadora
    draw.line([(80, 185), (W - 80, 185)], fill=colores['texto'], width=1)

    # Nombre del producto (puede ser largo, dividir en líneas)
    palabras = nombre.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        if len(linea_actual + " " + palabra) <= 18:
            linea_actual = (linea_actual + " " + palabra).strip()
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)

    y_nombre = 260 - (len(lineas) * 45) // 2
    for linea in lineas:
        draw.text((W // 2, y_nombre), linea,
                  fill=colores['texto'], font=font_nombre, anchor="mm")
        y_nombre += 50

    # Icono decorativo (círculo con símbolo de hoja)
    cx, cy, r = W // 2, 380, 50
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=colores['texto'], width=2)
    draw.text((cx, cy), "🌿", font=font_brand, anchor="mm")

    # Línea separadora inferior
    draw.line([(80, 460), (W - 80, 460)], fill=colores['texto'], width=1)

    # Advertencia sanitaria
    draw.text((W // 2, 490),
              "TABACO PARA LIAR",
              fill=colores['texto'], font=font_categoria, anchor="mm")
    draw.text((W // 2, 520),
              "Perjudicial para la salud",
              fill=colores['texto'], font=font_small, anchor="mm")

    return img


class Command(BaseCommand):
    help = 'Genera imágenes genéricas de packaging para todos los productos'

    def handle(self, *args, **options):
        if not PILLOW_OK:
            self.stdout.write(self.style.ERROR('Pillow no está instalado. Ejecutá: pip install pillow'))
            return

        # Crear carpeta media/productos si no existe
        media_productos = os.path.join(settings.MEDIA_ROOT, 'productos')
        os.makedirs(media_productos, exist_ok=True)

        productos = Producto.objects.all()
        if not productos.exists():
            self.stdout.write(self.style.WARNING('No hay productos en la base de datos.'))
            return

        for producto in productos:
            categoria_nombre = producto.categoria.nombre if producto.categoria else 'Tabaco Natural'
            nombre_archivo = f"producto_{producto.id}_{producto.nombre.lower().replace(' ', '_')}.png"
            ruta_archivo = os.path.join(media_productos, nombre_archivo)

            img = crear_imagen_producto(producto.nombre, categoria_nombre)
            img.save(ruta_archivo, 'PNG', quality=95)

            # Asignar la imagen al producto
            with open(ruta_archivo, 'rb') as f:
                producto.imagen.save(
                    nombre_archivo,
                    File(f),
                    save=True
                )

            self.stdout.write(self.style.SUCCESS(
                f'✓ Imagen generada para: {producto.nombre}'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ {productos.count()} imágenes generadas en media/productos/'
        ))
