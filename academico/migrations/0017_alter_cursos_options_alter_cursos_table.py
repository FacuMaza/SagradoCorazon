# Generated by Django 5.1 on 2024-09-03 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0016_alter_lugar_nacimiento_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cursos',
            options={'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
        migrations.AlterModelTable(
            name='cursos',
            table='Cursos',
        ),
    ]