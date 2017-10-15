from django.forms import ModelForm
from typer.core.models import Bet


class BetEventForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['wallet', 'chosen_result', 'value', ]