from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_eliminar_precio_mayorista'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen_2',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen_3',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
