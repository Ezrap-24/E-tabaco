from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        # ── Orden: nuevos campos + cambios ─────────────────
        migrations.AddField(
            model_name='orden',
            name='usuario',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ordenes',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name='orden',
            name='direccion_envio',
        ),
        migrations.AddField(
            model_name='orden',
            name='direccion',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='ciudad',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='region',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orden',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='orden',
            name='notas',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='fecha_pago',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orden',
            name='estado',
            field=models.CharField(
                choices=[
                    ('pendiente_pago', 'Pendiente de pago'),
                    ('pagado', 'Pagado'),
                    ('preparando', 'Preparando'),
                    ('enviado', 'Enviado'),
                    ('entregado', 'Entregado'),
                    ('cancelado', 'Cancelado'),
                ],
                default='pendiente_pago',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='orden',
            name='stripe_payment_intent',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        # ── DetallePedido ──────────────────────────────────
        migrations.AddField(
            model_name='detallepedido',
            name='producto_nombre',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
