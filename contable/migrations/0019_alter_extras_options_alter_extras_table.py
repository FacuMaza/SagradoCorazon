# Generated by Django 5.1 on 2024-11-14 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0018_extras_egreso_extras_ingreso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extras',
            options={'verbose_name': 'extra', 'verbose_name_plural': 'extras'},
        ),
        migrations.AlterModelTable(
            name='extras',
            table='extras',
        ),
    ]
