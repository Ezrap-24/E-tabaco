from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_imagen_2_imagen_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='dimensiones',
            field=models.CharField(
                blank=True, max_length=50,
                help_text='Ej: 6x15 cm. Usar para accesorios en lugar de peso.'
            ),
        ),
    ]
