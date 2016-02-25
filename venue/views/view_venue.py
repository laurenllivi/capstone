from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from homepage import models as hmod


def view_venue(request, listing_id):
    '''create new listing'''

    user = request.user

    listing = hmod.Listing.objects.get(id=listing_id)
    host = hmod.User.objects.get(id=listing.user_id)

    try:
        listing_features = hmod.Listing_Feature.objects.filter(feature_id=listing_id)
    except hmod.Listing_Feature.DoesNotExist:
        listing_features = None


    # get the images for this listing
    images = hmod.Listing_Photo.objects.filter(listing=listing)

    # the equivalent of template_vars in DMP
    context = {
        'images': images,
        'listing': listing,
        'host': host,
    }

    return render(request, 'venue/view_venue.html', context)