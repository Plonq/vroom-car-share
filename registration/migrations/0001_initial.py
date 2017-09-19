# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-14 06:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=50)),
                ('address_line2', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('VIC', 'Victoria'), ('NSW', 'New South Wales'), ('WA', 'Western Australia'), ('TAS', 'Tasmania'), ('QLD', 'Queensland'), ('SA', 'South Australia')], max_length=3)),
                ('postcode', models.CharField(max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16)),
                ('expiry_month', models.CharField(max_length=2)),
                ('expiry_year', models.CharField(max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_card', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]