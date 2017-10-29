from django.forms import ModelForm, widgets
from datetimewidget import widgets as ext_widgets
from typer.core.models import Bet, Event, Wallet


class BetEventForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['wallet', 'chosen_result', 'value', ]

    def __init__(self, *args, **kwargs):
        super(BetEventForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget.attrs['min'] = 1

    def clean(self):
        super(BetEventForm, self).clean()
        wallet = self.cleaned_data.get('wallet')
        if wallet.money < self.cleaned_data.get('value'):
            msg = 'Brak wystarczających środków w portfelu!'
            self.add_error('value', msg)
        elif self.cleaned_data.get('value') < 1:
            msg = 'Minimalna stawka zakładu wynosi 1!'
            self.add_error('value', msg)


class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['author', 'creation_time', 'open', 'result', ]
        widgets = {
            'start_time': ext_widgets.DateTimeWidget(attrs={id:'id_start_time'},
                                                     usel10n=True, bootstrap_version=3),
            'end_time': ext_widgets.DateTimeWidget(attrs={id:'id_end_time'},
                                                     usel10n=True, bootstrap_version=3)
        }


class CloseEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['result', ]