# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('temperatures', '0002_auto_20161206_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probe',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
