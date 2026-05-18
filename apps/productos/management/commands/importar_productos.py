from django.core.management.base import BaseCommand
from django.db import transaction
import pandas as pd
import os
from apps.productos.models import Producto, Categoria


class Command(BaseCommand):
    help = 'Importar productos desde Excel catalogo-productos-v3.xlsx'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("IMPORTAR PRODUCTOS DESDE EXCEL")
        self.stdout.write("=" * 60)

        excel_file = 'catalogo-productos-v3.xlsx'

        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f'\n✗ Archivo no encontrado: {excel_file}'))
            return

        try:
            # Leer Excel
            df = pd.read_excel(excel_file)
            self.stdout.write(self.style.SUCCESS(f'\n✓ Excel leído: {len(df)} productos\n'))

            # Crear/obtener categoría
            categoria, created = Categoria.objects.get_or_create(
                nombre='Tabacos',
                defaults={'descripcion': 'Tabaco y derivados'}
            )
            status = "creada" if created else "existe"
            self.stdout.write(self.style.SUCCESS(f'✓ Categoría "Tabacos" {status}\n'))

            # Importar con transacción
            with transaction.atomic():
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
                        activo = bool(row.get('activo', True))

                        if not nombre:
                            self.stdout.write(f'  ⚠ Fila {idx+2}: Nombre vacío')
                            errores += 1
                            continue

                        # Crear o actualizar
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
                                'imagen': f'products/{imagen_nombre}' if imagen_nombre else '',
                            }
                        )

                        if created:
                            creados += 1
                            self.stdout.write(f'  ✓ CREADO: {marca} - {nombre[:35]}')
                        else:
                            actualizados += 1
                            self.stdout.write(f'  ↻ ACTUALIZADO: {marca} - {nombre[:35]}')

                    except Exception as e:
                        errores += 1
                        self.stdout.write(self.style.ERROR(f'  ✗ Fila {idx+2}: {str(e)[:50]}'))

            # Resumen final
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write("RESUMEN")
            self.stdout.write("=" * 60)
            self.stdout.write(self.style.SUCCESS(f'✓ Creados: {creados}'))
            self.stdout.write(self.style.WARNING(f'↻ Actualizados: {actualizados}'))
            if errores > 0:
                self.stdout.write(self.style.ERROR(f'✗ Errores: {errores}'))

            total = Producto.objects.count()
            self.stdout.write(self.style.SUCCESS(f'\n✓ Total productos en BD: {total}'))
            self.stdout.write(self.style.SUCCESS('\n✓ Importación completada'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {e}'))
            import traceback
            traceback.print_exc()
