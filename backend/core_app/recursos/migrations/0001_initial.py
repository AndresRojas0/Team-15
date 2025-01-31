# Generated by Django 5.1.4 on 2025-01-26 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('planificacion_diaria', '0003_planificaciondiaria_unique_planificacion_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('url', models.URLField(verbose_name=500)),
                ('planificacion_diaria_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planificacion_diaria.planificaciondiaria')),
            ],
        ),
    ]
