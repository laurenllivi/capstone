from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.shortcuts import *
from homepage import models as hmod
from lib import choices
from django.template import RequestContext


def view_venue(request, listing_id):
    '''create new listing'''

    request_form = request_booking_form(request, listing_id)

    user = request.user

    listing = hmod.Listing.objects.get(id=listing_id)
    host = hmod.User.objects.get(id=listing.user_id)
    listing_features = hmod.Listing_Feature.objects.filter(listing_id=listing.id)
    features = []
    for feature in listing_features:
        new_feature = hmod.Feature.objects.get(id=feature.feature_id)
        features.append(new_feature.name)

    # get the images for this listing
    cover_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
    images = hmod.Listing_Photo.objects.filter(listing=listing)
<<<<<<< a935526c94329429c5cc60b8e893428e4ff674ea
    
    # get the reviews for this venue
    reviews = hmod.Review.objects.filter(listing=listing)
=======
    reviews = hmod.Review.objects.filter(listing=listing_id)
    for review in reviews:
        review.user = hmod.User.objects.get(id=review.user_id)
        review.starcount = round(int(review.rating * 2)) - 1  #minus one for the 0 index
>>>>>>> show reviews/ratings and set calendar with available dates

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
<<<<<<< a935526c94329429c5cc60b8e893428e4ff674ea
=======
        'range': range(10),  # 5 stars broken into 2 pieces each
>>>>>>> show reviews/ratings and set calendar with available dates
    }

    return render_to_response('venue/view_venue.html', context, RequestContext(request))

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
            try:
                if form.cleaned_data['start_time'] > form.cleaned_data['end_time']:
                    message = "End time must be later than start time."

                else:
                    #Creat booking request
                    rental_request = hmod.Rental_Request()
                    rental_request.request_date = form.cleaned_data['event_date']
                    rental_request.start_time = form.cleaned_data['start_time']
                    rental_request.end_time = form.cleaned_data['end_time']
                    rental_request.user_id = request.user.id
                    rental_request.listing_date_id = hmod.Listing_Date.objects\
                        .filter(listing_id=listing.id)\
                        .filter(date=rental_request.request_date)[0].id

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
        attrs={'class': 'datepicker', 'required': 'True'}
    ))
    start_time = forms.ChoiceField(widget=forms.Select(), choices=choices.TIME_CHOICES, required=True)

    end_time = forms.ChoiceField(widget=forms.Select(), choices=choices.TIME_CHOICES, required=True)
