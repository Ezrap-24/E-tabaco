#!/usr/bin/env python3
"""
Script2 de procesamiento de fotos — e-Tabaco
============================================
Qué hace este script:
  1. Lee imágenes HEIC/JPG de una carpeta de entrada
  2. Mejora la iluminación automáticamente
  3. Reduce reflejos y puntos brillantes
  4. Redimensiona a 800x800px para web
  5. Guarda como JPG optimizado en la carpeta de salida

Instalación de dependencias (ejecutar una sola vez en el CMD):
  pip install pillow pillow-heif numpy

Uso:
  1. Verificar que INPUT_FOLDER y OUTPUT_FOLDER al final del archivo sean correctos
  2. Ejecutar: python procesar_fotos2.py

Diferencia con procesar_fotos.py (Script1):
  Este script NO elimina el fondo con IA. Es más rápido y útil cuando
  el fondo ya es aceptable o se va a recortar manualmente después.
"""

import sys
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance

# ── Dependencias ───────────────────────────────────────────────────────────────

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("⚠️  pillow-heif no instalado. Las fotos HEIC no se podrán procesar.")
    print("   Instalá con: pip install pillow-heif\n")


# ── Funciones principales ──────────────────────────────────────────────────────

def mejorar_iluminacion(img_rgb):
    """
    Mejora la iluminación y reduce reflejos sobre toda la imagen RGB.

    Ajustes aplicados:
      - Auto niveles por canal: estira el rango tonal para mejor contraste
        ignorando el 2% de sombras y el 2% de luces extremas.
      - Recuperación de reflejos: atenúa suavemente los puntos muy brillantes
        (brillo promedio > 230/255) para recuperar detalle perdido.
      - Leve boost de saturación: compensa la pérdida de viveza que a veces
        produce el ajuste de niveles.
    """
    arr = np.array(img_rgb).astype(np.float32)

    # 1. Auto niveles por canal — estira contraste sin quemar colores
    for canal in range(3):
        p_min = np.percentile(arr[:, :, canal], 2)
        p_max = np.percentile(arr[:, :, canal], 98)
        if p_max > p_min:
            arr[:, :, canal] = np.clip(
                (arr[:, :, canal] - p_min) / (p_max - p_min) * 255,
                0, 255
            )

    # 2. Recuperación de reflejos — atenúa píxeles muy brillantes
    brillo = arr.mean(axis=2)
    mascara_reflejos = brillo > 230
    arr[mascara_reflejos] = arr[mascara_reflejos] * 0.82  # reducir 18% de brillo

    img_mejorada = Image.fromarray(arr.astype(np.uint8), 'RGB')

    # 3. Boost leve de saturación (1.15 = +15%) para compensar el ajuste de niveles
    img_mejorada = ImageEnhance.Color(img_mejorada).enhance(1.15)

    return img_mejorada


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
    print("-" * 50)

    exitosas = 0
    errores = 0

    for i, ruta_img in enumerate(sorted(imagenes), 1):
        try:
            print(f"[{i}/{len(imagenes)}] {ruta_img.name} ...", end=" ", flush=True)

            # 1. Abrir imagen
            img = Image.open(ruta_img).convert('RGB')

            # 2. Mejorar iluminación y reducir reflejos
            img_mejorada = mejorar_iluminacion(img)

            # 3. Redimensionar para web
            img_final = redimensionar_para_web(img_mejorada, tamaño)

            # 4. Guardar como JPG optimizado
            nombre_salida = ruta_img.stem + '.jpg'
            ruta_salida = salida / nombre_salida
            img_final.save(ruta_salida, 'JPEG', quality=85, optimize=True)

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
OUTPUT_FOLDER = r"C:\Users\YASITCOMPUTER\Documents\Claude Code\e-Tabaco\Fotos E-tabaco\procesadas2"
TAMAÑO_WEB    = 800

# ── Punto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    procesar_carpeta(INPUT_FOLDER, OUTPUT_FOLDER, TAMAÑO_WEB)
