# Generated by Django 5.1.4 on 2025-01-09 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planificacion_mensual', '0002_alter_planificacionmensual_planificacion_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionmensual',
            name='tipo_actividad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
