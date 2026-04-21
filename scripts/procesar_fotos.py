#!/usr/bin/env python3
"""
Script de procesamiento de fotos — e-Tabaco
============================================
Qué hace este script:
  1. Lee imágenes HEIC/JPG de una carpeta de entrada
  2. Elimina el fondo con IA (rembg) — funciona con cualquier color de fondo
  3. Mejora la iluminación automáticamente
  4. Reduce reflejos y puntos brillantes
  5. Reemplaza el fondo por blanco
  6. Redimensiona a 800x800px para web
  7. Guarda como JPG optimizado en la carpeta de salida

Instalación de dependencias (ejecutar una sola vez en el CMD):
  pip install pillow pillow-heif "rembg[cpu]" numpy

Uso:
  1. Verificar que INPUT_FOLDER y OUTPUT_FOLDER al final del archivo sean correctos
  2. Ejecutar: python procesar_fotos.py
  Nota: la primera vez descarga el modelo de IA (~170MB), es normal que tarde.
"""

import sys
import numpy as np
from pathlib import Path
from PIL import Image

# ── Dependencias ───────────────────────────────────────────────────────────────

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("⚠️  pillow-heif no instalado. Las fotos HEIC no se podrán procesar.")
    print("   Instalá con: pip install pillow-heif\n")

try:
    from rembg import remove, new_session
except ImportError:
    print("❌ rembg es obligatorio. Instalá con: pip install \"rembg[cpu]\"")
    sys.exit(1)


# ── Funciones principales ──────────────────────────────────────────────────────

def eliminar_fondo(img_pil, session):
    """
    Elimina el fondo usando IA (rembg / U2Net).
    Devuelve imagen RGBA con el fondo transparente.
    Funciona con cualquier color de fondo y respeta los colores del producto.
    """
    return remove(img_pil, session=session)


def mejorar_iluminacion(img_rgba):
    """
    Mejora la iluminación y reduce reflejos operando SOLO sobre el producto
    (píxeles no transparentes), sin tocar el fondo.

    Ajustes aplicados:
      - Auto niveles: estira el rango tonal para mejor contraste
      - Recuperación de reflejos: baja suavemente los puntos muy brillantes
    """
    arr = np.array(img_rgba).astype(np.float32)
    alpha = arr[:, :, 3]
    mascara = alpha > 10  # píxeles que son producto (no fondo transparente)

    if not mascara.any():
        return img_rgba

    rgb = arr[:, :, :3]

    # 1. Auto niveles — ajusta brillo/contraste usando solo los píxeles del producto
    for canal in range(3):
        valores = rgb[:, :, canal][mascara]
        p_min = np.percentile(valores, 2)   # ignorar el 2% más oscuro
        p_max = np.percentile(valores, 98)  # ignorar el 2% más brillante
        if p_max > p_min:
            rgb[:, :, canal] = np.clip(
                (rgb[:, :, canal] - p_min) / (p_max - p_min) * 255,
                0, 255
            )

    # 2. Recuperación de reflejos — detecta y suaviza puntos muy brillantes
    brillo = rgb.mean(axis=2)
    reflejos = (brillo > 230) & mascara  # solo en el producto, no en el fondo
    rgb[reflejos] = rgb[reflejos] * 0.82  # reducir 18% de brillo en reflejos

    arr[:, :, :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


def componer_sobre_blanco(img_rgba):
    """
    Pega la imagen RGBA sobre un fondo blanco y devuelve imagen RGB.
    """
    fondo = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
    fondo.paste(img_rgba, mask=img_rgba.split()[3])
    return fondo.convert("RGB")


def redimensionar_para_web(img, tamaño=800):
    """
    Redimensiona la imagen manteniendo proporción
    y la centra en un cuadrado de fondo blanco.
    Resultado: imagen cuadrada de tamaño x tamaño píxeles.
    """
    img.thumbnail((tamaño, tamaño), Image.LANCZOS)
    lienzo = Image.new('RGB', (tamaño, tamaño), (255, 255, 255))
    offset_x = (tamaño - img.width) // 2
    offset_y = (tamaño - img.height) // 2
    lienzo.paste(img, (offset_x, offset_y))
    return lienzo


def procesar_carpeta(carpeta_entrada, carpeta_salida, tamaño=800):
    """
    Procesa todas las imágenes en carpeta_entrada
    y guarda los resultados en carpeta_salida.
    """
    entrada = Path(carpeta_entrada)
    salida = Path(carpeta_salida)
    salida.mkdir(parents=True, exist_ok=True)

    extensiones = {'.heic', '.jpg', '.jpeg', '.png',
                   '.HEIC', '.JPG', '.JPEG', '.PNG'}

    imagenes = [f for f in entrada.iterdir() if f.suffix in extensiones]

    if not imagenes:
        print(f"❌ No se encontraron imágenes en: {carpeta_entrada}")
        print("   Verificá que la ruta sea correcta y que haya archivos HEIC o JPG.")
        return

    print(f"\n📸 Imágenes encontradas: {len(imagenes)}")
    print(f"📁 Guardando en: {carpeta_salida}")
    print("⏳ Cargando modelo de IA... (solo tarda la primera vez)\n")
    print("-" * 50)

    # Cargar el modelo una sola vez — más eficiente para muchas imágenes
    session = new_session("u2net")

    exitosas = 0
    errores = 0

    for i, ruta_img in enumerate(sorted(imagenes), 1):
        try:
            print(f"[{i}/{len(imagenes)}] {ruta_img.name} ...", end=" ", flush=True)

            # 1. Abrir imagen
            img = Image.open(ruta_img).convert('RGB')

            # 2. Eliminar fondo con IA → devuelve RGBA
            img_rgba = eliminar_fondo(img, session)

            # 3. Mejorar iluminación y reducir reflejos (opera sobre RGBA)
            img_rgba = mejorar_iluminacion(img_rgba)

            # 4. Componer sobre fondo blanco → RGB
            img_rgb = componer_sobre_blanco(img_rgba)

            # 5. Redimensionar para web
            img_final = redimensionar_para_web(img_rgb, tamaño)

            # 6. Guardar como JPG
            nombre_salida = ruta_img.stem + '.jpg'
            ruta_salida = salida / nombre_salida
            img_final.save(ruta_salida, 'JPEG', quality=85)

            print(f"✓ → {nombre_salida}")
            exitosas += 1

        except Exception as e:
            print(f"✗ Error: {e}")
            errores += 1

    print("-" * 50)
    print(f"\n✅ Proceso completado.")
    print(f"   Exitosas : {exitosas}")
    if errores:
        print(f"   Con error: {errores}")
    print(f"\nLas imágenes procesadas están en:\n  {carpeta_salida}\n")


# ── CONFIGURACIÓN ──────────────────────────────────────────────────────────────

INPUT_FOLDER  = r"C:\Users\YASITCOMPUTER\Documents\Claude Code\e-Tabaco\Fotos E-tabaco"
OUTPUT_FOLDER = r"C:\Users\YASITCOMPUTER\Documents\Claude Code\e-Tabaco\Fotos E-tabaco\procesadas"
TAMAÑO_WEB    = 800

# ── Punto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    procesar_carpeta(INPUT_FOLDER, OUTPUT_FOLDER, TAMAÑO_WEB)
