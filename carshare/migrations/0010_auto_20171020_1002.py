# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-19 23:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0009_auto_20171011_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='due',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='paid',
        ),
    ]