# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-12-01 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(default='hello', unique=True),
            preserve_default=False,
        ),
    ]
