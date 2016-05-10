from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
import datetime as dt
from datetime import timedelta
from decimal import *

@login_required
def my_past_events(request):
    
    user = request.user

    past_events = format_event_requests(request, user)
        
    context = {
        'user': user,
        'eventlisthtml': past_events.content,
    }
    return render_to_response('account/my_past_events.html', context, RequestContext(request))


def format_event_requests(request, user):

    form = SubmitReviewForm(initial={
        'description': ''
    })

    if request.method == 'POST':

        if 'SubmitReview' in request.POST:

            event_id = request.POST['event_id']
            event = hmod.Rental_Request.objects.get(id=event_id)

            rating_name = 'starModal' + str(event_id)
            try:
                star_rating = Decimal(request.POST[rating_name]) / Decimal(2)
            except Exception:
                star_rating = 0

            new_review, was_created = hmod.Review.objects.get_or_create(
                listing_id=event.listing_id,
                event=event,
                user=user)
            new_review.rating = star_rating

            form = SubmitReviewForm(request.POST)
            if form.is_valid():
                description = form.cleaned_data['description']
                new_review.description = description

            new_review.save()
            form = SubmitReviewForm(initial={
                'description': ''
            })

    event_requests = hmod.Rental_Request.objects.filter(user=user)

    venue_pics_dict = {}
    reviews_dict = {}
    star_count_dict = {}

    event_list = []

    for event_request in event_requests:
        listing = event_request.listing
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
            # and add it to the dictionary
            venue_pics_dict[listing.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass

        try:
            review = hmod.Review.objects.filter(event_id=event_request.id).filter(user=user).first()
            if review:
                reviews_dict[event_request.id] = review.description
                star_count_dict[event_request.id] = (Decimal(review.rating) * 2) - 1 #minus one for the 0 index of the iterator

        except hmod.Review.DoesNotExist:
            pass

    date_threshold = dt.datetime.now() - timedelta(days=1)

    events = hmod.Rental_Request.objects\
        .filter(user=user)\
        .exclude(approved=False)\
        .exclude(canceled=True)\
        .filter(listing_date__date__lt=date_threshold)

    for e in events:
        event_list.append(e)

    context = {
        'user': user,
        'event_list': event_list,
        'venue_pics_dict': venue_pics_dict,
        'reviews_dict': reviews_dict,
        'star_count_dict': star_count_dict,
        'rating_range': range(10),  # 5 stars broken into 2 pieces each
        'form': form,
    }

    return render_to_response('account/past_event_list.html', context, RequestContext(request))


class SubmitReviewForm(forms.Form):
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        'rows': '5',
    }), required=False)