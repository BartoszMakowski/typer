from django.forms import ModelForm
from typer.core.models import Bet, Event


class BetEventForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['wallet', 'chosen_result', 'value', ]


class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['author', 'creation_time', 'closed', 'result', ]