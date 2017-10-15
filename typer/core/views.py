from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet, Event


def index(request):
    if request.user.is_authenticated():
        user = request.user
        wallets = Wallet.objects.filter(owner=user).all()
        return render(request, 'user/home.html.j2',
                      {'username': user.username,
                       'wallets': wallets})
    else:
        return HttpResponse("INDEX PAGE")


def wallet_info(request, wallet_id):
    if request.user.is_authenticated():
        user = request.user
        wallet = Wallet.objects.get(id=wallet_id)
        return render(request, 'wallet/info.html.j2',
                      {'username': user.username,
                       'wallet': wallet})
    else:
        return HttpResponse("WALLET INFO PAGE")


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/index.html.j2',
                  {'events': events})

def event_info(request, event_id):
    event = Event.objects.get(id=event_id)
    fields = Event._meta.get_fields()
    return render(request, 'event/info.html.j2',
                  {'event': event,
                   'fields': fields})


