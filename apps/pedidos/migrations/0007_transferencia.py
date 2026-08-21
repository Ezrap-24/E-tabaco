from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_transbank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='metodo_pago',
            field=models.CharField(
                choices=[
                    ('webpay', 'Webpay Plus (Transbank)'),
                    ('mercadopago', 'Mercado Pago'),
                    ('transferencia', 'Transferencia Bancaria / Depósito'),
                ],
                default='mercadopago',
                max_length=20,
            ),
        ),
    ]
