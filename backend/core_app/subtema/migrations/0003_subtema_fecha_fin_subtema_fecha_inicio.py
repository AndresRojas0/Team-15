# Generated by Django 5.1.4 on 2025-01-04 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtema', '0002_remove_subtema_fecha_fin_remove_subtema_fecha_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtema',
            name='fecha_fin',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='subtema',
            name='fecha_inicio',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
