from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0007_transferencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='tipo_documento',
            field=models.CharField(
                choices=[('boleta', 'Boleta'), ('factura', 'Factura')],
                default='boleta',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='orden',
            name='razon_social',
            field=models.CharField(blank=True, max_length=200, verbose_name='Razón Social'),
        ),
        migrations.AddField(
            model_name='orden',
            name='giro',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='orden',
            name='rut_facturacion',
            field=models.CharField(blank=True, max_length=15, verbose_name='RUT'),
        ),
    ]
