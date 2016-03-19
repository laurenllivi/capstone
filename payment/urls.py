from django.conf.urls import url
from payment import views

urlpatterns = [
    url(r'^cc_info/$', views.cc_info, name='cc_info'),
    url(r'^cc_info/(?P<rental_request_id>[0-9]+)/$', views.cc_info, name='cc_info'),
    url(r'^success/(?P<rental_request_id>[0-9]+)/$', views.success, name='success'),
]