from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

BET_SIDE = (
    (0, 'X'),
    (1, '1'),
    (2, '2')
)


class Wallet(models.Model):
    owner = models.ForeignKey(User, null=False)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    money = models.FloatField(blank=False)
    active = models.BooleanField(default=True, blank=False)
    creation_time = models.DateTimeField(default=datetime.now)
    template = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.name


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
    result = models.IntegerField(null=True, blank=True)


class Bet(models.Model):
    wallet = models.ForeignKey(Wallet, null=False)
    chosen_result = models.IntegerField(blank=False, choices=BET_SIDE)
    event = models.ForeignKey(Event, null=False)
    value = models.FloatField(blank=False)
    odd = models.FloatField(blank=False)
    reward = models.FloatField(blank=False)
    creation_time = models.DateTimeField(default=datetime.now, blank=False)
    open = models.BooleanField(default=True, blank=False)
    won = models.NullBooleanField(null=True, blank=True)