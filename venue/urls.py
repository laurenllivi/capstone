from django.conf.urls import url
from venue import views

urlpatterns = [
    url(r'^manage_venue/(?P<listing_id>[0-9]+)/$', views.manage_venue, name='manage_venue'),
]