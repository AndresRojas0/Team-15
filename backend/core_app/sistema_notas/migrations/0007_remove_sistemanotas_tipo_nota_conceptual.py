# Generated by Django 5.1.4 on 2025-01-08 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_notas', '0006_alter_sistemanotas_tipo_nota_conceptual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sistemanotas',
            name='tipo_nota_conceptual',
        ),
    ]
