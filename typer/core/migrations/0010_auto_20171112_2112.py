# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 20:12
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20171101_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptance', models.BooleanField(verbose_name='Akceptacja znajomości')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to=settings.AUTH_USER_MODEL, verbose_name='Znajomy')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL, verbose_name='Osoba')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='home_odd',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0, 'Minimalny kurs wynosi 1.0.')], verbose_name='Kurs na zwycięstwo gospodarzy'),
        ),
    ]
