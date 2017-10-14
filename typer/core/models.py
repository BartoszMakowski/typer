from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Wallet(models.Model):
    owner = models.ForeignKey(User, null=False)
    money = models.FloatField(blank=False)
    active = models.BooleanField(default=True, blank=False)
    creation_time = models.DateTimeField(default=datetime.now)


class Event(models.Model):
    author = models.ForeignKey(User, null=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    creation_time = models.DateTimeField(default=datetime.now, blank=False)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    home_name = models.CharField(max_length=50, blank=False)
    away_name = models.CharField(max_length=50, blank=False)
    home_odd = models.FloatField(default=1.0, blank=False)
    away_odd = models.FloatField(default=1.0, blank=False)
    draw_odd = models.FloatField(default=1.0, blank=False)
    closed = models.BooleanField(default=False, blank=False)
    result = models.IntegerField(blank=True)


class Bet(models.Model):
    wallet = models.ForeignKey(Wallet, null=False)
    event = models.ForeignKey(Event, null=False)
    value = models.FloatField(blank=False)
    odd = models.FloatField(blank=False)
    reward = models.FloatField(blank=False)
    creation_time = models.DateTimeField(default=datetime.now, blank=False)
    open = models.BooleanField(default=True, blank=False)
    won = models.BooleanField(blank=True)