from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.shortcuts import *
from homepage import models as hmod
from lib import choices
from django.template import RequestContext
from datetime import datetime
import pytz
from pytz import timezone
from tzwhere import tzwhere

def view_venue(request, listing_id):
    '''create new listing'''

    request_form = request_booking_form(request, listing_id)
    policies = get_cancellation_policies(request)

    user = request.user

    listing = hmod.Listing.objects.get(id=listing_id)
    host = hmod.User.objects.get(id=listing.user_id)
    listing_policy = hmod.Listing_Policy.objects.get(listing_id=listing.id)
    cancellation_policy = hmod.Cancellation_Policy.objects.get(id=listing_policy.cancellation_policy_id)

    listing_features = hmod.Listing_Feature.objects.filter(listing_id=listing.id)
    features = []
    for feature in listing_features:
        new_feature = hmod.Feature.objects.get(id=feature.feature_id)
        features.append(new_feature.name)

    # get the images for this listing
    cover_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
    images = hmod.Listing_Photo.objects.filter(listing=listing)
    
    # get the reviews for this venue
    reviews = hmod.Review.objects.filter(listing_id=listing_id)
    average_rating = 0
    if reviews:
        average_rating = reviews[0].rating

        for review in reviews:
            review.user = hmod.User.objects.get(id=review.user_id)
            review.starcount = round(int(review.rating * 2)) - 1  #minus one for the 0 index of the iterator
            average_rating = (average_rating + review.rating)/2
    else:
        average_rating = 0

    # the equivalent of template_vars in DMP
    context = {
        'cover_pic': cover_pic,
        'images': images,
        'image_count': len(images),
        'listing': listing,
        'host': host,
        'formhtml': request_form.content,
        'features': features,
        'reviews': reviews,
        'range': range(10),  # 5 stars broken into 2 pieces each
        'average_rating': average_rating,
        'cancellation_policy': cancellation_policy,
        'policieshtml': policies.content,
    }

    return render_to_response('venue/view_venue.html', context, RequestContext(request))

def get_cancellation_policies(request):
    cancellation_policies = hmod.Cancellation_Policy.objects.all()

    context = {
        'policies': cancellation_policies
    }

    return render_to_response('partials/_cancellation_policy.html', context, RequestContext(request))

def request_booking_form(request, listing_id):

    listing = hmod.Listing.objects.get(id=listing_id)
    listing_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id).values_list('date')
    date_strings = []
    for date in listing_dates:
        date = date[0].strftime('%m/%d/%Y')
        date_strings.append(date)

    form = RequestBookingForm()
    message = ''

    if request.method == 'POST':
        form = RequestBookingForm(request.POST)

        if form.is_valid():
            if not request.user.is_authenticated():
                message = 'You must be logged in to request a reservation.'
            else:

                try:
                    if form.cleaned_data['start_time'] > form.cleaned_data['end_time']:
                        message = "End time must be later than start time."

                    else:
                        #Create booking request
                        rental_request = hmod.Rental_Request()
                        event_date = form.cleaned_data['event_date']
                        rental_request.start_time = form.cleaned_data['start_time']
                        rental_request.end_time = form.cleaned_data['end_time']
                        rental_request.user_id = request.user.id
                        rental_request.listing = hmod.Listing.objects.get(id=listing_id)
                        rental_request.listing_date_id = hmod.Listing_Date.objects\
                            .filter(listing_id=listing.id)\
                            .filter(date=event_date)[0].id
                        rental_request.request_date = datetime.now()

                        tz = listing.timezone
                        event_start = str(event_date) + " " + str(rental_request.start_time)
                        start_datetime = datetime.strptime(event_start, "%Y-%m-%d %H:%M")
                        # add venue's timezone to start time
                        #local_dt = timezone(tz).localize(start_datetime, is_dst=None)
                        print(">>>>>>>>>>>")
                        print("The line above is the one with the error for me.")

                        #rental_request.start_datetime = local_dt
                        rental_request.start_datetime = start_datetime

                        rental_request.save()

                        message = 'Request Has Been Sent!'
                except:
                    message = 'Invalid Input'

        else:
            message = 'Invalid Input'

    context = {
        'listing': listing,
        'listing_dates': date_strings,
        'form': form,
        'message': message,
    }

    return render_to_response('venue/request_form.html', context, RequestContext(request))


class RequestBookingForm(forms.Form):
    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'id': 'event-date', 'class': 'datepicker', 'required': 'True'}
    ))
    start_time = forms.ChoiceField(widget=forms.Select(
        attrs={'id': 'start-time', 'required': 'True'}
    ), choices=choices.TIME_CHOICES, required=True)

    end_time = forms.ChoiceField(widget=forms.Select(
        attrs={'id': 'end-time', 'required': 'True'}
    ), choices=choices.TIME_CHOICES, required=True)
