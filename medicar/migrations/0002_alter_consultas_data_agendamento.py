# Generated by Django 3.2.8 on 2021-11-05 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultas',
            name='data_agendamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicar.agendas'),
        ),
    ]
