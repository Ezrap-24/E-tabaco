from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_producto_dimensiones'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='seccion',
            field=models.CharField(
                blank=True, max_length=50,
                help_text='Sección del nav: Tabacos, Accesorios, etc.'
            ),
        ),
    ]
