from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
from django import forms
from homepage import models as hmod
from django.contrib.auth.decorators import login_required
from lib import convert_date_string as convert_date

@login_required
def post_venue(request, listing_id):
    '''actually post the venue for all to see!'''
    
    user = request.user
    listing = hmod.Listing.objects.get(id=listing_id)
    images = hmod.Listing_Photo.objects.filter(listing_id=listing_id)
    image_count = hmod.Listing_Photo.objects.filter(listing_id=listing_id).count()
    available_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id)
    features = hmod.Listing_Feature.objects.filter(listing_id=listing.id)
    listing_policy = hmod.Listing_Policy.objects.get(listing_id=listing.id)
    cancellation_policy = hmod.Cancellation_Policy.objects.get(id=listing_policy.cancellation_policy.id)
    
    # if the list of available dates is empty
    if not available_dates:
        dates_available = "None"
    else:
        # use my method to convert the list of objects into a string of dates
        dates_available = convert_date.convert_db_into_date_string(available_dates)
            
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
        'dates_available': dates_available,
        'images': images,
        'image_count': image_count,
        'features': features,
        'cancellation_policy': cancellation_policy,
    }

    return render_to_response('venue/post_venue.html', context, RequestContext(request))
    
@login_required
def post_venue__unlist(request, listing_id):
    ''' unlist a venue '''
    
    listing = hmod.Listing.objects.get(id=listing_id)
    listing.currently_listed = False
    listing.save()
    
    return HttpResponseRedirect('/account/my_venues/')
    

