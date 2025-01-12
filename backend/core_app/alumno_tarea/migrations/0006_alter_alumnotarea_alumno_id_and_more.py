# Generated by Django 5.1.4 on 2025-01-11 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0001_initial'),
        ('alumno_tarea', '0005_alter_alumnotarea_alumno_id_and_more'),
        ('tarea_asignada', '0003_rename_materia_tareaasignada_materia_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnotarea',
            name='alumno_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alumno_tareas', to='alumno.alumno'),
        ),
        migrations.AlterField(
            model_name='alumnotarea',
            name='tarea_asignada_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alumno_tareas', to='tarea_asignada.tareaasignada'),
        ),
    ]
