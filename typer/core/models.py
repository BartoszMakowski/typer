from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

BET_SIDE = (
    (0, 'X'),
    (1, '1'),
    (2, '2')
)


class Wallet(models.Model):
    owner = models.ForeignKey(User, null=False,
                              verbose_name='Właściciel portfela')
    name = models.CharField(max_length=100, blank=False,
                            verbose_name='Nazwa portfela')
    description = models.TextField(blank=True,
                                   verbose_name='Opis portfela')
    money = models.FloatField(blank=False,
                              verbose_name='Saldo')
    active = models.BooleanField(default=True, blank=False,
                                 verbose_name='Portfel jest aktywny')
    creation_time = models.DateTimeField(default=datetime.now,
                                         verbose_name='Czas utworzenia')
    template = models.BooleanField(default=False, blank=False,
                                   verbose_name='Portfel-szablon')

    def __str__(self):
        return self.name

    def get_lifetime(self):
        return (timezone.now() - self.creation_time).days


class Event(models.Model):
    author = models.ForeignKey(User, null=False,
                               verbose_name='Autor wydarzenia')
    start_time = models.DateTimeField(blank=False,
                                      verbose_name='Czas rozpoczęcia wydarzenia')
    end_time = models.DateTimeField(blank=False,
                                    verbose_name='Czas zakończenia wydarzenia')
    creation_time = models.DateTimeField(default=datetime.now, blank=False,
                                         verbose_name='Czas utworzenia wydarzenia')
    name = models.CharField(max_length=100, blank=False,
                            verbose_name='Nazwa wydarzenia')
    description = models.TextField(blank=True,
                                   verbose_name='Opis wydarzenia')
    home_name = models.CharField(max_length=50, blank=False,
                                 verbose_name='Nazwa zespołu gospodarzy')
    away_name = models.CharField(max_length=50, blank=False,
                                 verbose_name='Nazwa zespołu gości')
    home_odd = models.FloatField(default=1.0, blank=False,
                                 verbose_name='Kurs na zwycięstwo gospodarzy',
                                 validators=[MinValueValidator(1.0, 'Minimalny kurs wynosi 1.0.')])
    draw_odd = models.FloatField(default=1.0, blank=False,
                                 verbose_name='Kurs na remis',
                                 validators=[MinValueValidator(1.0, 'Minimalny kurs wynosi 1.0.')])
    away_odd = models.FloatField(default=1.0, blank=False,
                                 verbose_name='Kurs na zwycięstwo gości',
                                 validators=[MinValueValidator(1.0, 'Minimalny kurs wynosi 1.0.')])
    open = models.BooleanField(default=True, blank=False,
                               verbose_name='Wydarzenie nierozliczone')
    result = models.IntegerField(null=True, blank=True,
                                 verbose_name='Wynik wydarzenia',
                                 choices=BET_SIDE)

    def is_active(self):
        return self.start_time <= timezone.now() and self.end_time > timezone.now()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('can_close', "Can insert result and close event."),
        )


class Bet(models.Model):
    wallet = models.ForeignKey(Wallet, null=False,
                               verbose_name='Portfel')
    chosen_result = models.IntegerField(blank=False, choices=BET_SIDE,
                                        verbose_name='Typowany wynik')
    event = models.ForeignKey(Event, null=False,
                              verbose_name='Typowane wydarzenie')
    value = models.FloatField(blank=False,
                              verbose_name='Stawka zakładu',
                              validators=[MinValueValidator(0.0, 'Wartość zakładu nie może być ujemna!')])
    odd = models.FloatField(blank=False,
                            verbose_name='Kurs zakładu')
    reward = models.FloatField(blank=False,
                               verbose_name='Możlwa wygrana')
    creation_time = models.DateTimeField(default=datetime.now, blank=False,
                                         verbose_name='Czas utworzenia')
    open = models.BooleanField(default=True, blank=False,
                               verbose_name='Zakład nierozliczony')
    won = models.NullBooleanField(null=True, blank=True,
                                  verbose_name='Zakład wygrany')

    def __str__(self):
        return 'Zakład: ' + self.event.name


class Friendship(models.Model):
    person = models.ForeignKey(User, null=False,
                                verbose_name='Osoba', related_name='person')
    friend = models.ForeignKey(User, null=False,
                               verbose_name='Znajomy', related_name='friend')
    acceptance = models.BooleanField(null=False, verbose_name='Akceptacja znajomości')