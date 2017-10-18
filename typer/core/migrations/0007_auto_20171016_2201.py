# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_bet_chosen_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='chosen_result',
            field=models.IntegerField(choices=[(0, 'draw'), (1, 'home'), (2, 'away')]),
        ),
    ]