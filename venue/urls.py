from django.conf.urls import url
from venue import views

urlpatterns = [
    url(r'^manage_venue/(?P<listing_id>[0-9]+)/$', views.manage_venue, name='manage_venue'),
    url(r'^manage_venue/$', views.manage_venue, name='manage_venue'),
    url(r'^find_venue/$', views.find_venue, name='find_venue'),
    url(r'^update_find/$', views.find_venue_form, name='update_find_form'),
    url(r'^test/$', views.test, name='test'),
    url(r'^manage_venue__del_img/(?P<listing_id>[0-9]+)/(?P<image_id>[0-9]+)/$', views.manage_venue__del_img, name='manage_venue__del_img'),
    url(r'^post_venue/(?P<listing_id>[0-9]+)/$', views.post_venue, name='post_venue'),
    url(r'^post_venue__unlist/(?P<listing_id>[0-9]+)/$', views.post_venue__unlist, name='post_venue__unlist'),
]