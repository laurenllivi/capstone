from django.conf.urls import url
from venue import views

urlpatterns = [
    url(r'^manage_venue/(?P<listing_id>[0-9]+)/$', views.manage_venue, name='manage_venue'),
    url(r'^manage_venue/$', views.manage_venue, name='manage_venue'),
    url(r'^find_venue/$', views.find_venue, name='find_venue'),
    url(r'^calendar/$', views.calendar, name='calendar'),
]