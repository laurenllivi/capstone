from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
from django import forms
from lib import choices
from homepage import models as hmod
from django.contrib.auth.decorators import login_required
import geocoder
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D #shortcut for distance
from django.template import RequestContext
import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder


def find_venue(request, city=None, category=None):
    '''search for a venue'''

    response = find_venue_form(request, city, category)

    context = {
        'formhtml': response.content,
    }

    return render_to_response('venue/find_venue.html', context, RequestContext(request))


def find_venue_form(request, city=None, category=None):

    if city:
        search_location = city
    else:
        search_location = 'Provo, Ut, United States'
    if category:
        venue_type = category
    else:
        venue_type = 'backyard'

    price_per_hour_range = [0, 5000]
    event_date = None
    distance = 5
    
    # get the list of favorite venues
    # favorites = hmod.Favorite_Listing.objects.filter(user_id=request.user.id)
    # favorite_venues_list = hmod.Listing.objects.filter(id__in=favorites)
    
    form = FindVenueForm(initial={
        'location': search_location,
        'venue_type': venue_type,
        'price_per_hour_lower': price_per_hour_range[0],
        'price_per_hour_upper': price_per_hour_range[1],
    })

    if request.method == 'POST':
        form = FindVenueForm(request.POST)
        # lower = request.POST.get('lower', '')
        # upper = request.POST.get('upper', '')

        if form.is_valid():
            distance = form.cleaned_data['within_miles']
            search_location = form.cleaned_data['location']
            venue_type = form.cleaned_data['venue_type']
            # price_per_hour_range = [lower, upper]
            price_per_hour_range = [form.cleaned_data['price_per_hour_lower'],
                                    form.cleaned_data['price_per_hour_upper']]
            event_date = form.cleaned_data['event_date']

    g = geocoder.google(search_location)
    search_geo = Point(float(g.lat), float(g.lng))

    pnt = GEOSGeometry(search_geo)
    venue_list = hmod.Listing.objects\
        .filter(geolocation__distance_lte=(pnt, D(mi=distance)))\
        .filter(category__iexact=venue_type)\
        .filter(price_per_hour__gte=price_per_hour_range[0])\
        .filter(price_per_hour__lte=price_per_hour_range[1])\
        .filter(currently_listed=True)

    if event_date:
        venues = []
        for venue in venue_list:
            if hmod.Listing_Date.objects.filter(date=event_date, listing_id=venue.id).exists():
                venues.append(venue)

    else:
        venues = venue_list

    venue_pics_dict = {}
    venue_locations_dict = {}
    for venue in venues:
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=venue).first()
            # and add it to the dictionary
            venue_pics_dict[venue.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass

        venue_html = "<a href='/venue/view_venue/" + str(venue.id) + "'>"\
                     "<img class='venue-pic' src='/static/images/venue-images/" \
                     + str(venue.id) + "/" \
                     + str(venue_pic) + "'/>" \
                     + "<div class='dot-title'>" + venue.title + "</div>"\
                     + "</a>"
        try:
            venue_locations_dict[venue.id] = {
                "lat": venue.geolocation.x,
                "lon": venue.geolocation.y,
                "title": venue_html
            }

        except:
            pass

        #get the user's favorites from this venue
        if hmod.Favorite_Listing.objects.filter(listing=venue, user=request.user).exists():
            venue.favorite = True
        else:
            venue.favorite = False


    search_location = json.dumps(search_location)
    location_data = json.dumps(venue_locations_dict)  # lat and lon of venues

    context = {
        'form': form,
        'search_location': search_location,
        'venues': venues,
        'venue_pics_dict': venue_pics_dict,
        'location_data': location_data,
        'price_per_hour_range': price_per_hour_range,
        # 'favorite_venues_list': favorite_venues_list,
    }
    return render_to_response('venue/venue_results.html', context, RequestContext(request))

def find_venue__update_favorite(request, venue_id, favorited):
    '''adds a venue to the user's list of favorite venues'''

    listing = hmod.Listing.objects.get(id=venue_id)

    if favorited == 'true':
        '''create favorite object if it does not already exist'''
        hmod.Favorite_Listing.objects.get_or_create(listing=listing, user=request.user)
    else:
        try:
            favoriteObj = hmod.Favorite_Listing.objects.get(listing=listing, user=request.user)
            favoriteObj.delete()
        except hmod.Favorite_Listing.DoesNotExist:
            pass

    return HttpResponse('')

class FindVenueForm(forms.Form):
    within_miles = forms.ChoiceField(required=False, widget=forms.Select(attrs={'id': 'venue-distance'}), label="Within", choices=choices.WITHIN_MILES_CHOICES)
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'location-search-autocomplete ui-autocomplete-input ui-corner-all'
    }))
    event_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    price_per_hour = forms.IntegerField(required=False, widget=forms.TextInput())
    price_per_hour_lower = forms.IntegerField(required=False)
    price_per_hour_upper = forms.IntegerField(required=False)