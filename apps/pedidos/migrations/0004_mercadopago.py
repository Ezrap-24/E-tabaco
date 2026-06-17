from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_correlativo_y_contador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='stripe_payment_intent',
        ),
        migrations.AddField(
            model_name='orden',
            name='mp_preference_id',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.AddField(
            model_name='orden',
            name='mp_payment_id',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
    ]
