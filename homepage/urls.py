from django.conf.urls import url
from homepage import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^faq/$', views.faq, name='faq'),
]