# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20171015_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='won',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='result',
            field=models.IntegerField(null=True),
        ),
    ]
