# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-12-28 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20191226_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job_type',
            new_name='employment_type',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='expiry',
            new_name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='job',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='job',
            name='job_category',
        ),
        migrations.RemoveField(
            model_name='job',
            name='skills',
        ),
        migrations.AlterField(
            model_name='job',
            name='education',
            field=models.CharField(blank=True, choices=[('HS', 'High School/GRE'), ('AS', "Associate's"), ('BA/BS', "Bachelor's"), ('MA/MS', "Master's"), ('PHD', 'Doctorate')], max_length=255, null=True),
        ),
    ]
