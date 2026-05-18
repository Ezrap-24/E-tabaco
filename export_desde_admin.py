"""
Exporta todos los productos a productos_export.csv
Uso: python export_desde_admin.py
"""
import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etabaco.settings')
django.setup()

from apps.productos.models import Producto

campos = [
    'id', 'nombre', 'marca', 'codigo', 'categoria', 'intensidad',
    'peso_gramos', 'procedencia', 'descripcion',
    'precio_unidad', 'precio_mayor', 'cantidad_minima_mayor',
    'stock', 'activo', 'destacado', 'creado',
]

with open('productos_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(campos)
    for p in Producto.objects.select_related('categoria').all():
        writer.writerow([
            p.id, p.nombre, p.marca, p.codigo,
            p.categoria.nombre if p.categoria else '',
            p.intensidad, p.peso_gramos, p.procedencia, p.descripcion,
            p.precio_unidad, p.precio_mayor, p.cantidad_minima_mayor,
            p.stock, p.activo, p.destacado, p.creado,
        ])

print(f'Exportados {Producto.objects.count()} productos -> productos_export.csv')
