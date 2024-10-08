# Generated by Django 5.1 on 2024-10-01 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0002_alter_matricula_options_alter_matricula_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='pagomatricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efectivo', models.FloatField()),
                ('transferencia', models.FloatField()),
                ('cheque', models.FloatField()),
                ('pagare', models.FloatField()),
                ('matriculas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contable.matricula')),
            ],
            options={
                'verbose_name': 'pagomatricula',
                'verbose_name_plural': 'pagomatriculas',
                'db_table': 'pagomatriculas',
            },
        ),
    ]
