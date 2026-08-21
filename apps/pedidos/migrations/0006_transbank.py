from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_costo_envio'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='metodo_pago',
            field=models.CharField(
                choices=[('mercadopago', 'Mercado Pago'), ('webpay', 'Webpay Plus (Transbank)')],
                default='mercadopago',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='orden',
            name='tbk_token',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.AddField(
            model_name='orden',
            name='tbk_authorization_code',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
