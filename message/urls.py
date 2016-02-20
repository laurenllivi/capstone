from django.conf.urls import url
from message import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^message_home/$', views.message_home, name='message_home'),
   
]