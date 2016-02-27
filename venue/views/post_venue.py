from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
from django import forms
from homepage import models as hmod
from django.contrib.auth.decorators import login_required

@login_required
def post_venue(request, listing_id):
    '''actually post the venue for all to see!'''
    
    user = request.user
    listing = hmod.Listing.objects.get(id=listing_id)
    images = hmod.Listing_Photo.objects.filter(listing_id=listing_id)
    image_count = hmod.Listing_Photo.objects.filter(listing_id=listing_id).count()
    available_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id)
    
    # if the list of available dates is empty
    if not available_dates:
        available_dates = "None"
    
    # make sure that only the owner of the venue can access this page
    # (since the venue ID is passed through the URL)
    if user.id != listing.user.id:
        return HttpResponseRedirect('/homepage/error_message')
    
    if request.method == 'POST':
        listing.currently_listed = True
        listing.save()
        
        return HttpResponseRedirect('/account/my_venues/')

    context = {
        'listing': listing,
        'user': user,
        'available_dates': available_dates,
        'images': images,
        'image_count': image_count,
    }

    return render_to_response('venue/post_venue.html', context, RequestContext(request))
    
@login_required
def post_venue__unlist(request, listing_id):
    ''' unlist a venue '''
    
    listing = hmod.Listing.objects.get(id=listing_id)
    listing.currently_listed = False
    listing.save()
    
    return HttpResponseRedirect('/account/my_venues/')
    

