from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wallet/(?P<wallet_id>[0-9]+)/$', views.wallet_info, name='wallet info'),
    url(r'^event/$', views.event_list, name='event list'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_info, name='event info'),
    url(r'^event/new/$', views.event_new, name='event new'),
]