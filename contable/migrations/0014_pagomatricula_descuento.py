# Generated by Django 5.1 on 2024-11-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0013_recibo_pagado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagomatricula',
            name='descuento',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
