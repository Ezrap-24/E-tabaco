from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_mercadopago'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='costo_envio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
