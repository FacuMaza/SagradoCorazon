# Generated by Django 5.1 on 2024-09-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0030_alter_tutores_vive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutores',
            name='Vive',
            field=models.CharField(choices=[('S', 'Si'), ('N', 'No')], max_length=1),
        ),
    ]
