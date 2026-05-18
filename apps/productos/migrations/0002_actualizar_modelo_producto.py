from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        # Quitar campos del modelo viejo
        migrations.RemoveField(model_name='producto', name='precio_caja'),
        migrations.RemoveField(model_name='producto', name='unidades_por_caja'),

        # Agregar campos nuevos
        migrations.AddField(
            model_name='producto',
            name='marca',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='intensidad',
            field=models.CharField(
                blank=True,
                choices=[('Suave', 'Suave'), ('Medio', 'Medio'), ('Intenso', 'Intenso')],
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='producto',
            name='peso_gramos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='procedencia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_mayor',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Precio por mayor (mínimo cantidad_minima_mayor unidades)',
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='producto',
            name='cantidad_minima_mayor',
            field=models.IntegerField(
                default=3,
                help_text='Cantidad mínima para acceder al precio mayorista',
            ),
        ),

        # Modificar campos existentes
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={
                'ordering': ['marca', 'nombre'],
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
