# Generated by Django 2.2.5 on 2020-01-16 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_auto_20200114_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employment_type',
            field=models.CharField(blank=True, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Contract', 'Contract')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_frequency',
            field=models.CharField(blank=True, choices=[('Per-Hour', 'Per-Hour'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], max_length=225, null=True),
        ),
    ]
