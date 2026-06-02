"""
Normaliza imágenes de accesorios a media/products/
Convención: marca-tipo-variante.jpg (todo minúsculas, sin espacios, sin caracteres especiales)

Uso:
    python scripts/normalizar_accesorios.py
    python scripts/normalizar_accesorios.py --dry-run   (solo muestra qué haría)
"""

import shutil
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
ORIGEN_FILTROS = BASE / "static" / "img" / "Fotos Productos" / "Accesorios" / "Filtros"
ORIGEN_PAPELILLOS = BASE / "static" / "img" / "Fotos Productos" / "Accesorios" / "Papelillos"
DESTINO = BASE / "media" / "products"

DRY_RUN = "--dry-run" in sys.argv

# ─────────────────────────────────────────────────────────────
# MAPA DE RENOMBRADO
# Clave: nombre original del archivo (case-insensitive match)
# Valor: nombre normalizado en media/products/
# Solo se copian los archivos listados aquí.
# ─────────────────────────────────────────────────────────────

MAPA_FILTROS = {
    # OCB Filtros
    "OCB-FILTRO-REGULAR.JPG":              "ocb-filtro-regular.jpg",
    "OCB-FILTRO-REGULAR-CAJA.JPG":         "ocb-filtro-regular-caja.jpg",
    "OCB-FILTRO-SLIM-ENGOMADO.JPG":        "ocb-filtro-slim-engomado.jpg",
    "OCB-FILTRO-SLIM-ENGOMADO-CAJA.JPG":   "ocb-filtro-slim-engomado-caja.jpg",
    "OCB-FILTRO-SLIM-LARGO.JPG":           "ocb-filtro-slim-largo.jpg",
    "OCB-FILTRO-SLIM-LARGO-CAJA.JPG":      "ocb-filtro-slim-largo-caja.jpg",
    "OCB-FILTRO-VIRGIN.JPG":               "ocb-filtro-virgin.jpg",
    "OCB-FILTRO-VIRGIN-CAJA.JPG":          "ocb-filtro-virgin-caja.jpg",
    "OCB-FILTRO-CANAMO.JPG":               "ocb-filtro-canamo.jpg",
    "OCB-FILTRO-CANAMO-CAJA.JPG":          "ocb-filtro-canamo-caja.jpg",
    "OCB-FILTRO-X.jpg":                    "ocb-filtro-x.jpg",
    "OCB-FILTRO-X-CAJA.jpg":               "ocb-filtro-x-caja.jpg",
    # Stream Click
    "FILTRO-STREAM-CLICK-ARANDANO.JPG":    "stream-filtro-click-arandano.jpg",
    "FILTRO-STREAM-CLICK-ORANGE.JPG":      "stream-filtro-click-orange.jpg",
    "FILTRO-STREAM-CLICK-SANDIA.JPG":      "stream-filtro-click-sandia.jpg",
    "FILTRO-STREAM-CLICK-TCarbón.JPG":     "stream-filtro-click-carbon.jpg",
    # Redfield
    "FILTRO-REDFIELD-SLIM-150.JPG":        "redfield-filtro-slim.jpg",
    "FILTRO-REDFIELD-LONG-SLIM-150.JPG":   "redfield-filtro-slim-largo.jpg",
    "FILTRO-REDFIELD-SLIM-MENTHOL-150.JPG":"redfield-filtro-slim-mentol.jpg",
    "FILTRO-REDFIELDBIO-150.JPG":          "redfield-filtro-bio.jpg",
    # Golden
    "FILTRO-GOLDEN100CLIC.JPG":            "golden-filtro-clic-100.jpg",
    "FILTRO-GOLDENBIO200.JPG":             "golden-filtro-bio-200.jpg",
}

MAPA_PAPELILLOS = {
    # OCB Premium — solo cerrado como imagen principal
    "OCB-PREMIUM-#1-cerrado.JPG":          "ocb-papelillo-premium-n1.jpg",
    "OCB-PREMIUM-#1-abierto.JPG":          "ocb-papelillo-premium-n1-abierto.jpg",
    "OCB-PREMIUM-#1-caja.JPG":             "ocb-papelillo-premium-n1-caja.jpg",
    "OCB-PREMIUM-11-4-cerrado.JPG":        "ocb-papelillo-premium-1-14.jpg",
    "OCB-PREMIUM-11-4-abierto.JPG":        "ocb-papelillo-premium-1-14-abierto.jpg",
    "OCB-PREMIUM-11-4-caja.JPG":           "ocb-papelillo-premium-1-14-caja.jpg",
    # OCB Virgin
    "OCB-VIRGIN-#1-cerrado.JPG":           "ocb-papelillo-virgin-n1.jpg",
    "OCB-VIRGIN-#1-abierto.JPG":           "ocb-papelillo-virgin-n1-abierto.jpg",
    "OCB-VIRGIN-#1-caja.JPG":             "ocb-papelillo-virgin-n1-caja.jpg",
    "OCB-VIRGIN-11-4-cerrado.JPG":         "ocb-papelillo-virgin-1-14.jpg",
    "OCB-VIRGIN-11-4-abierto.JPG":         "ocb-papelillo-virgin-1-14-abierto.jpg",
    "OCB-VIRGIN-11-4-caja.JPG":            "ocb-papelillo-virgin-1-14-caja.jpg",
    # OCB Cáñamo
    "OCB-CANAMO #1-cerrado.JPG":           "ocb-papelillo-canamo-n1.jpg",
    "OCB-CANAMO #1-abierto.JPG":           "ocb-papelillo-canamo-n1-abierto.jpg",
    "OCB-CANAMO #1-caja.JPG":              "ocb-papelillo-canamo-n1-caja.jpg",
    "OCB-CANAMO-11-4-cerrado.JPG":         "ocb-papelillo-canamo-1-14.jpg",
    "OCB-CANAMO-11-4-abierto.JPG":         "ocb-papelillo-canamo-1-14-abierto.jpg",
    "OCB-CANAMO-11-4-caja.JPG":            "ocb-papelillo-canamo-1-14-caja.jpg",
    # Mantra sabores
    "Papelillos-MANTRA-Chicle-1-¼.JPG":    "mantra-papelillo-chicle.jpg",
    "Papelillos-MANTRA-Chocolate-1-¼.JPG": "mantra-papelillo-chocolate.jpg",
    "Papelillos-MANTRA-Coco-1-¼.JPG":      "mantra-papelillo-coco.jpg",
    "Papelillos-MANTRA-Frutilla-1-¼.JPG":  "mantra-papelillo-frutilla.jpg",
    "Papelillos-MANTRA-Menta-1-¼-1022x1024.JPG": "mantra-papelillo-menta.jpg",
    "Papelillos-MANTRA-Uva-1-¼.JPG":       "mantra-papelillo-uva.jpg",
    "Papelillos-MANTRA-Vainilla-1-¼-.JPG": "mantra-papelillo-vainilla.jpg",
}


def copiar(origen_dir: Path, mapa: dict):
    copiados = 0
    omitidos = 0
    for nombre_original, nombre_nuevo in mapa.items():
        origen = origen_dir / nombre_original
        destino = DESTINO / nombre_nuevo

        if not origen.exists():
            print(f"  ⚠  NO ENCONTRADO: {nombre_original}")
            omitidos += 1
            continue

        if destino.exists():
            print(f"  ↷  YA EXISTE (skip): {nombre_nuevo}")
            omitidos += 1
            continue

        if DRY_RUN:
            print(f"  →  {nombre_original}  →  {nombre_nuevo}")
        else:
            shutil.copy2(origen, destino)
            print(f"  ✓  {nombre_nuevo}")
        copiados += 1

    return copiados, omitidos


def main():
    if DRY_RUN:
        print("=== DRY RUN — no se copia nada ===\n")
    else:
        DESTINO.mkdir(parents=True, exist_ok=True)

    print("── Filtros ──────────────────────────────")
    c1, o1 = copiar(ORIGEN_FILTROS, MAPA_FILTROS)

    print("\n── Papelillos ───────────────────────────")
    c2, o2 = copiar(ORIGEN_PAPELILLOS, MAPA_PAPELILLOS)

    total_copiados = c1 + c2
    total_omitidos = o1 + o2
    accion = "por copiar" if DRY_RUN else "copiados"
    print(f"\n{'='*45}")
    print(f"  {accion}: {total_copiados}   |   omitidos/ya existían: {total_omitidos}")
    if not DRY_RUN and total_copiados > 0:
        print(f"  Destino: {DESTINO}")


if __name__ == "__main__":
    main()
