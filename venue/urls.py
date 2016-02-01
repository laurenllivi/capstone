from django.conf.urls import url
from venue import views

urlpatterns = [
    url(r'^post_venue/$', views.post_venue, name='post_venue'),
]