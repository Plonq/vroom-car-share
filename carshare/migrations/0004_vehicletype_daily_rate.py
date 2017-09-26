# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-26 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0003_auto_20170926_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletype',
            name='daily_rate',
            field=models.DecimalField(decimal_places=2, default=80.0, max_digits=6),
            preserve_default=False,
        ),
    ]
