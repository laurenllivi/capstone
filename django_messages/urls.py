from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from django_messages.views import *

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'^inbox/$', inbox, name='messages_inbox'),
    url(r'^outbox/$', outbox, name='messages_outbox'),
    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^search_messages/(?P<search_terms>.+)/$', search_messages, name='search_messages'),
    url(r'^search_messages/$', search_messages),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/(?P<listing>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    url(r'^trash/$', trash, name='messages_trash'),
)
