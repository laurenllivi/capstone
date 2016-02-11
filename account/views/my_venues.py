from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from django.template.defaulttags import register

# used to get a dictionary value by key (in the template)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def my_venues(request):
    
    user = request.user
    my_venues = hmod.Listing.objects.filter(user=user)
    
    venue_pics_dict = {}
    
    # get a picture for each venue
    for venue in my_venues:
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=venue).first()
            # and add it to the dictionary
            venue_pics_dict[venue.id] = venue_pic 
            print(">>>>>>>>>>>>>>>>>>>>>>>")
            print(venue_pics_dict)
        
        except hmod.Listing_Photo.DoesNotExist:
            pass
        
    context = {
        'user': user,
        'my_venues': my_venues,
        'venue_pics_dict': venue_pics_dict,
        
    }
    return render(request, 'account/my_venues.html', context)