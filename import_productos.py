#!/usr/bin/env python
"""
Script para importar productos desde Excel a Django
Uso: python manage.py shell < import_productos.py
O: python import_productos.py (si está en el mismo nivel que manage.py)
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etabaco.settings')
django.setup()

import pandas as pd
from apps.productos.models import Producto, Categoria
from django.core.files.base import ContentFile

print("=" * 60)
print("IMPORTAR PRODUCTOS DESDE EXCEL")
print("=" * 60)

# Ruta del Excel
excel_file = 'catalogo-productos-v3.xlsx'

try:
    # Leer Excel
    df = pd.read_excel(excel_file)
    print(f"\n✓ Excel leído: {len(df)} productos\n")

    # Crear/obtener categoría "Tabacos"
    categoria, created = Categoria.objects.get_or_create(
        nombre='Tabacos',
        defaults={'descripcion': 'Tabaco y derivados'}
    )
    if created:
        print(f"✓ Categoría 'Tabacos' creada")
    else:
        print(f"✓ Categoría 'Tabacos' existe")

    # Importar productos
    creados = 0
    actualizados = 0
    errores = 0

    for idx, row in df.iterrows():
        try:
            marca = str(row.get('marca', '')).strip()
            nombre = str(row.get('nombre', '')).strip()
            imagen_nombre = str(row.get('imagen', '')).strip()
            precio = float(row.get('precio_unidad', 0)) if row.get('precio_unidad') else 5000
            stock = int(row.get('stock', 50)) if row.get('stock') else 50
            activo = row.get('activo', True)

            if not nombre:
                print(f"  ⚠ Fila {idx+2}: Nombre vacío, saltada")
                continue

            # Buscar imagen en media/products
            media_path = os.path.join('media', 'products', imagen_nombre)

            # Crear o actualizar producto
            producto, created = Producto.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'marca': marca,
                    'precio_unidad': precio,
                    'stock': stock,
                    'activo': activo,
                    'categoria': categoria,
                    'intensidad': 'Medio',
                    'peso_gramos': 45,
                    'procedencia': 'Chile',
                }
            )

            # Asignar imagen si existe
            if imagen_nombre and os.path.exists(media_path):
                # Si no tiene imagen o necesita actualizar
                if not producto.imagen or not os.path.exists(os.path.join('media', str(producto.imagen))):
                    producto.imagen = f'products/{imagen_nombre}'
                    producto.save()

            if created:
                creados += 1
                print(f"  ✓ {idx+1}. CREADO: {marca} - {nombre[:30]}")
            else:
                actualizados += 1
                print(f"  ↻ {idx+1}. ACTUALIZADO: {marca} - {nombre[:30]}")

        except Exception as e:
            errores += 1
            print(f"  ✗ Fila {idx+2}: Error - {str(e)[:50]}")

    # Resumen
    print(f"\n" + "=" * 60)
    print(f"RESUMEN")
    print(f"=" * 60)
    print(f"✓ Creados: {creados}")
    print(f"↻ Actualizados: {actualizados}")
    print(f"✗ Errores: {errores}")
    print(f"Total en BD: {Producto.objects.count()}")
    print(f"\n✓ Importación completada")

except Exception as e:
    print(f"\n✗ Error general: {e}")
    import traceback
    traceback.print_exc()
