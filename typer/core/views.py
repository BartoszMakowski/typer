from django.shortcuts import render
from django.http import HttpResponse
from .models import Wallet


def index(request):
    if request.user.is_authenticated():
        user = request.user
        wallets = Wallet.objects.filter(owner=user).all()
        return render(request, 'user/home.html.j2',
                      {'username': user.username,
                       'wallets': wallets})

    else:
        return HttpResponse("INDEX PAGE")
