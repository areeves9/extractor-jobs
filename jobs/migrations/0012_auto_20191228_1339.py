# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-12-28 21:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20191228_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country', verbose_name='country'),
        ),
    ]
