from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
import re

@login_required
def favorites(request):

    user = request.user

    if request.method == 'POST':

        request_string = str(request.POST)
        if 'removeFavorite' in request_string:
            listing_id = re.search('removeFavorite(\d+)', request_string).group(1)

        try:
            favoriteObj = hmod.Favorite_Listing.objects.get(listing_id=listing_id, user=request.user)
            favoriteObj.delete()
        except hmod.Favorite_Listing.DoesNotExist:
            pass

    favoriteshtml = format_listings(request, user)

    context = {
        'favorites': favoriteshtml.content
    }

    return render_to_response('account/favorites.html', context, RequestContext(request))

def format_listings(request, user):
    favorites = hmod.Favorite_Listing.objects.filter(user=user).values('listing_id')
    listings = hmod.Listing.objects.filter(id__in=favorites)

    venue_pics_dict = {}

    for listing in listings:
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
            # and add it to the dictionary
            venue_pics_dict[listing.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass

    context = {
        'user': user,
        'favorite_listings': listings,
        'venue_pics_dict': venue_pics_dict,
    }

    return render_to_response('account/favorite_venue_list.html', context, RequestContext(request))



