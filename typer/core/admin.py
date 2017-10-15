from django.contrib import admin
from .models import Bet, Event, Wallet


admin.site.register([Bet, Event, Wallet])
