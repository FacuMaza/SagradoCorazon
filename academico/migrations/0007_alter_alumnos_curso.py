# Generated by Django 5.1 on 2024-09-18 21:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0006_alter_alumnos_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnos',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academico.cursos'),
        ),
    ]
