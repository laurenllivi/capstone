from django.conf.urls import url
from account import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_photo/$', views.profile_photo, name='profile_photo'),
    url(r'^profile_photo__del_img/$', views.profile_photo__del_img, name='profile_photo__del_img'),
    url(r'^public_profile/(?P<user_id>[0-9]+)/$', views.public_profile, name='public_profile'),
    url(r'^verification/$', views.verification, name='verification'),
    url(r'^profile_reviews/$', views.profile_reviews, name='profile_reviews'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^reset_confirmation/$', views.reset_confirmation, name='reset_confirmation'),
    #url(r'^reset_confirmation/$', TemplateView.as_view(template_name='account/reset_confirmation.html')),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),

    url(r'^my_venues/$', views.my_venues, name='my_venues'),
    url(r'venue_requests/$', views.venue_requests, name='venue_requests'),
    url(r'request_list/$', views.format_ven_requests, name='format_ven_requests'),
    url(r'^payment_preferences/$', views.payment_preferences, name='payment_preferences'),

    url(r'^my_events/$', views.my_events, name='my_events'),
    url(r'^my_events__del_rental_request/(?P<rental_request_id>[0-9]+)/$', views.my_events__del_rental_request, name='my_events__del_rental_request'),
    url(r'^my_past_events/$', views.my_past_events, name='my_past_events'),
    # url(r'^my_past_events__submit_review/(?P<event_id>[0-9]+)/$', views.my_past_events__submit_review, name='my_past_events__submit_review'),
    url(r'event_list/$', views.format_event_requests, name='format_event_requests'),

    url(r'favorites/$', views.favorites, name='favorites'),
]