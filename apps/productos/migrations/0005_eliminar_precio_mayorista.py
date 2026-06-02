from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_alter_producto_destacado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='precio_mayor',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='cantidad_minima_mayor',
        ),
    ]
