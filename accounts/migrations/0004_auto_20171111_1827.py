# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-11 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20171107_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='expiry_month',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=2),
        ),
    ]