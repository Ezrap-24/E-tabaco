"""
Utilidad para aplicar sello de agua a imágenes de productos.
Texto "purotabaco.cl" esquina inferior derecha, blanco semitransparente.
"""
from PIL import Image, ImageDraw, ImageFont


TEXTO = "purotabaco.cl"
OPACIDAD = 160      # 0-255
COLOR = (255, 255, 255, OPACIDAD)
MARGEN = 14         # píxeles desde el borde


def _obtener_fuente(tamaño: int):
    """Intenta cargar una fuente del sistema, fallback a la default de Pillow."""
    fuentes_candidatas = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for ruta in fuentes_candidatas:
        try:
            return ImageFont.truetype(ruta, tamaño)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def aplicar_sello(ruta_imagen: str) -> None:
    """Aplica el sello en esquina inferior derecha, in-place."""
    with Image.open(ruta_imagen).convert("RGBA") as img:
        ancho, alto = img.size

        # Fuente pequeña y discreta
        tamaño_fuente = max(12, ancho // 22)
        fuente = _obtener_fuente(tamaño_fuente)

        capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(capa)

        # Medir texto
        bbox = draw.textbbox((0, 0), TEXTO, font=fuente)
        texto_w = bbox[2] - bbox[0]
        texto_h = bbox[3] - bbox[1]

        # Posición: esquina inferior derecha con margen
        x = ancho - texto_w - MARGEN
        y = alto - texto_h - MARGEN

        # Sombra sutil para legibilidad sobre fondos claros
        draw.text((x + 1, y + 1), TEXTO, font=fuente, fill=(0, 0, 0, 80))
        # Texto principal
        draw.text((x, y), TEXTO, font=fuente, fill=COLOR)

        resultado = Image.alpha_composite(img, capa).convert("RGB")
        resultado.save(ruta_imagen, "WEBP", quality=82)
