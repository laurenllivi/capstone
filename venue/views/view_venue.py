from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.shortcuts import *
from homepage import models as hmod
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

    # the equivalent of template_vars in DMP
    context = {
        'cover_pic': cover_pic,
        'images': images,
        'image_count': len(images),
        'listing': listing,
        'host': host,
        'formhtml': request_form.content,
        'features': features,
    }

    return render_to_response('venue/view_venue.html', context, RequestContext(request))

def request_booking_form(request, listing_id):

    listing = hmod.Listing.objects.get(id=listing_id)
    form = RequestBookingForm()
    message = ''

    if request.method == 'POST':
        print('method was post')
        # event_date = form.cleaned_data['event_date']
        # start_time = form.cleaned_data['start_time']
        # end_time = form.cleaned_data['end_time']

        # SEND REQUEST FOR BOOKING

        message = 'Request Has Been Sent!'

    context = {
        'listing': listing,
        'form': form,
        'message': message,
    }

    return render_to_response('venue/request_form.html', context, RequestContext(request))


class RequestBookingForm(forms.Form):
    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'datepicker', 'required': True}
    ))
    start_time = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'timepicker', 'required': True}
    ))
    end_time = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'timepicker', 'required': True}
    ))
