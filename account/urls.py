from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^new_user/$', views.new_user, name='new_user'),
]