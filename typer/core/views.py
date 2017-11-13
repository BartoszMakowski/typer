from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Wallet, Event, Bet
from .forms import BetEventForm, NewEventForm, CloseEventForm


# based on: https://fragmentsofcode.wordpress.com/2008/12/08/django-group_required-decorator/
def group_required(group):
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name=group)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='/typer')


@login_required(login_url='/login')
def index(request):
    user = request.user
    wallets = Wallet.objects.filter(owner=user)
    events = Event.objects.filter(start_time__gte=timezone.now(), open=True)
    user_active_events = get_user_active_events(user)
    events_to_close = Event.objects.filter(end_time__lte=timezone.now(), open=True)
    return render(request, 'user/home.html.j2',
                  {'username': user.username,
                   'wallets': wallets,
                   'events': events,
                   'active_events': user_active_events,
                   'events_to_close': events_to_close})


@login_required(login_url='/login')
def wallet_list(request):
    wallets = Wallet.objects.filter(owner=request.user)
    return render(request, 'wallet/index.html.j2',
                  {'wallets': wallets,
                   'username': request.user.username,
                   })


@login_required(login_url='/login')
def wallet_info(request, wallet_id):
    user = request.user
    wallet = Wallet.objects.get(id=wallet_id)
    # if wallet.owner != user and not user.is_superuser:
    #     messages.error(request, 'Nie jesteś właścicielem tego portfela!')
    #     return HttpResponseRedirect('/typer/')
    bets = Bet.objects.filter(wallet=wallet)
    open_bets = bets.filter(open=True).all()
    closed_bets = bets.filter(open=False).all()
    return render(request, 'wallet/info.html.j2',
                  {'username': user.username,
                   'wallet': wallet,
                   'open_bets': open_bets,
                   'closed_bets': closed_bets})


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
    if event.end_time < timezone.now() and event.open:
        event.to_close = True
    else:
        event.to_close = False
    fields = Event._meta.get_fields()
    bets = Bet.objects.filter(event=event_id)
    template_data = {'event': event,
                     'fields': fields,
                     'bets': bets,
                     'username': request.user.username, }
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
            bet.reward = round(bet.value * bet.odd, 2)
            bet.save()
            messages.success(request, 'Twój zakład został przyjęty.')
            return HttpResponseRedirect(".")
    else:
        bet_form = BetEventForm()
        bet_form.fields['wallet'].queryset = Wallet.objects.filter(owner=request.user)
    if event.open and event.start_time > timezone.now():
        template_data['bet_form'] = bet_form
        # if not request.user.is_superuser:
        #     bets = bets.filter(wallet__owner=request.user)
        #     template_data['bets'] = bets
    return render(request, 'event/info.html.j2', template_data)


@group_required('Event admins')
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
            messages.success(request, 'Wydarzenie zostało dodane')
            return HttpResponseRedirect("/typer/event")
        else:
            messages.error(request, 'Wydarzenie nie zostało dodane. Popraw błędy w formularzu.')
    return render(request, 'event/new.html.j2', template_data)


@login_required(login_url='/login')
def event_close(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.end_time > timezone.now():
        messages.warning(request, 'Nie można zamnkąć wydarzenia, które jeszcze trwa!')
        return HttpResponseRedirect('..')
    event_close_form = CloseEventForm()
    bets = Bet.objects.filter(event=event_id).all()
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
            messages.success(request, 'Wydarzenie zostało zamknięta w powiązane z nim zakłady - pomyślnie rozliczone')
            return HttpResponseRedirect("/typer/event/" + event_id + "/")
        else:
            messages.error(request, 'Nie udało się zamknąć wydarzenia.')
    return render(request, 'event/close.html.j2', template_data)


@login_required(login_url='/login')
def ranking_list(request):
    wallets = Wallet.objects.all()
    return render(request, 'ranking/index.html.j2',
                  {'wallets': wallets,
                   'username': request.user.username,
                   })


def get_user_active_bets(user):
    active_bets = Bet.objects.filter(wallet__owner=user, event__start_time__lte=timezone.now(),
                                     event__end_time__gte=timezone.now())
    return active_bets



def get_user_active_events(user):
    active_bets = get_user_active_bets(user)
    active_events = [bet.event for bet in active_bets]
    return active_events