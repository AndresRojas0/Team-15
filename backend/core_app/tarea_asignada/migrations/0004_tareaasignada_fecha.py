# Generated by Django 5.1.4 on 2025-01-11 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarea_asignada', '0003_rename_materia_tareaasignada_materia_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tareaasignada',
            name='fecha',
            field=models.DateField(null=True),
        ),
    ]
