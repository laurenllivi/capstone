from django.conf.urls import url
from account import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^reset_confirmation/$', TemplateView.as_view(template_name='account/reset_confirmation.html')),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    
    
]