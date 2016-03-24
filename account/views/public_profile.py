from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from localflavor.us.forms import USPhoneNumberField
from django.core.validators import validate_email

def public_profile(request, user_id):

    user = hmod.User.objects.get(id=user_id)
    venues = hmod.Listing.objects.filter(user_id=user.id).filter(currently_listed=True)
    venue_pics_dict = {}

    # get a picture for each venue
    for venue in venues:
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=venue).first()
            # and add it to the dictionary
            venue_pics_dict[venue.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass


    context = {
        'user': user,
        'venues': venues,
        'venue_pics_dict': venue_pics_dict,
    }
    return render(request, 'account/public_profile.html', context)