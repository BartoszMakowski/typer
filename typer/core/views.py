from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Wallet, Event, Bet
from .forms import BetEventForm, NewEventForm


def index(request):
    if request.user.is_authenticated():
        user = request.user
        wallets = Wallet.objects.filter(owner=user).all()
        events = Event.objects.filter(start_time__gte=datetime.now(), closed=False)
        return render(request, 'user/home.html.j2',
                      {'username': user.username,
                       'wallets': wallets,
                       'events': events})
    else:
        return HttpResponse("INDEX PAGE")


def wallet_info(request, wallet_id):
    if request.user.is_authenticated():
        user = request.user
        wallet = Wallet.objects.get(id=wallet_id)
        bets = Bet.objects.filter(wallet=wallet)
        open_bets = bets.filter(open=True).all()
        closed_bets = bets.filter(open=False).all()
        return render(request, 'wallet/info.html.j2',
                      {'username': user.username,
                       'wallet': wallet,
                       'open_bets': open_bets,
                       'closed_bets': closed_bets})
    else:
        return HttpResponse("WALLET INFO PAGE")


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/index.html.j2',
                  {'events': events})

def event_info(request, event_id):
    event = Event.objects.get(id=event_id)
    fields = Event._meta.get_fields()
    bets = Bet.objects.filter(event=event_id)
    template_data = {'event': event,
                     'fields': fields,
                     'bets': bets}
    if request.method == 'POST':
        bet_form = BetEventForm(request.POST)
        if bet_form.is_valid():
            bet = bet_form.save(commit=False)
            bet.event = event
            if bet.chosen_result == 0:
                bet.odd = event.draw_odd
            elif bet.chosen_result == 1:
                bet.odd = event.home_odd
            elif bet.chosen_result == 2:
                bet.odd = event.away_odd
            if bet.value > bet.wallet.money:
                #TODO: not enough money
                pass
            else:
                bet.wallet.money -= bet.value
                bet.wallet.save()
            bet.reward = bet.value * bet.odd
            bet.open = True
            bet.save()
            return HttpResponseRedirect(".")

    else:
        if not event.closed:
            bet_form = BetEventForm()
            bet_form.fields['wallet'].queryset = Wallet.objects.filter(owner=request.user)
            template_data['bet_form'] = bet_form
    return render(request, 'event/info.html.j2', template_data)

def event_new(request):
    event_form = NewEventForm()
    template_data = {
        'event_form': event_form,
    }
    if request.method == 'POST':
        event_form = BetEventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.author = request.user
            event.save()
            return HttpResponseRedirect("/typer/event")
    return render(request, 'event/new.html.j2', template_data)
