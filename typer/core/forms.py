from django.forms import ModelForm, widgets
from datetimewidget import widgets as ext_widgets
from typer.core.models import Bet, Event


class BetEventForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['wallet', 'chosen_result', 'value', ]


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