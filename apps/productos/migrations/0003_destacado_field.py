from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_actualizar_modelo_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='destacado',
            field=models.BooleanField(
                default=False,
                help_text='Marcar para mostrar en la seccion de destacados del home',
            ),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad_minima_mayor',
            field=models.IntegerField(
                default=3,
                help_text='Cantidad minima para acceder al precio mayorista',
            ),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_mayor',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Precio por mayor (minimo cantidad_minima_mayor unidades)',
                max_digits=10,
                null=True,
            ),
        ),
    ]
