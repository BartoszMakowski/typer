from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Wallet, Event, Bet
from .forms import BetEventForm, NewEventForm, CloseEventForm

@login_required(login_url='/login')
def index(request):
    if request.user.is_authenticated():
        user = request.user
        wallets = Wallet.objects.filter(owner=user).all()
        events = Event.objects.filter(start_time__gte=datetime.now(), open=True)
        return render(request, 'user/home.html.j2',
                      {'username': user.username,
                       'wallets': wallets,
                       'events': events})

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/index.html.j2',
                  {'events': events,
                   'username': request.user.username,
                   })

@login_required(login_url='/login')
def event_info(request, event_id):
    event = Event.objects.get(id=event_id)
    fields = Event._meta.get_fields()
    bets = Bet.objects.filter(event=event_id)
    template_data = {'event': event,
                     'fields': fields,
                     'bets': bets,
                     'username': request.user.username,}
    if request.session.get('alert', False):
        template_data['alert'] = request.session.get('alert', False)
        request.session['alert'] = False
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

            bet.wallet.money -= bet.value
            bet.wallet.save()
            bet.reward = bet.value * bet.odd
            bet.open = True
            bet.save()
            return HttpResponseRedirect(".")
        else:
            alert = {
                'type': 'danger',
                'text': bet_form.errors
            }
            request.session['alert'] = alert
            return HttpResponseRedirect(".")

    else:
        if event.open:
            bet_form = BetEventForm()
            bet_form.fields['wallet'].queryset = Wallet.objects.filter(owner=request.user)
            template_data['bet_form'] = bet_form
    return render(request, 'event/info.html.j2', template_data)

@login_required(login_url='/login')
def event_new(request):
    event_form = NewEventForm()
    template_data = {
        'event_form': event_form,
        'username': request.user.username,
    }
    if request.method == 'POST':
        event_form = NewEventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.author = request.user
            event.save()
            return HttpResponseRedirect("/typer/event")
        else:
            print(event_form.errors)
    return render(request, 'event/new.html.j2', template_data)

@login_required(login_url='/login')
def event_close(request, event_id):
    event_close_form = CloseEventForm()
    bets = Bet.objects.filter(event=event_id).all()
    print(bets)
    template_data = {
        'event_close_form': event_close_form,
        'username': request.user.username,
        'bets': bets
    }
    if request.method == 'POST':
        event_close_form = CloseEventForm(request.POST)
        if event_close_form.is_valid():
            event = Event.objects.get(pk=event_id)
            event.result = event_close_form.cleaned_data['result']
            event.open = False
            event.save()
            for bet in bets:
                if bet.chosen_result == event.result:
                    bet.won = True
                    bet.wallet.money += bet.reward
                    bet.wallet.save()
                else:
                    bet.won = False
                bet.open = False
                bet.save()
            return HttpResponseRedirect("/typer/event/" + event_id + "/")
        else:
            print(event_close_form.errors)
    return render(request, 'event/close.html.j2', template_data)
