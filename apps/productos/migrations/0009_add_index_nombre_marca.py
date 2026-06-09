from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_producto_seccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='producto',
            name='marca',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
