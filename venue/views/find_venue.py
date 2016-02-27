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
import json


def find_venue(request):
    '''search for a venue'''

    response = find_venue_form(request)

    context = {
        'formhtml': response.content,
    }

    return render_to_response('venue/find_venue.html', context, RequestContext(request))


def find_venue_form(request):

    search_location = 'Provo, Ut, United States'
    venue_type = 'Backyard'
    price_per_hour_range = [0, 5000]

    form = FindVenueForm(initial={
        'location': search_location,
        'price_per_hour_lower': price_per_hour_range[0],
        'price_per_hour_upper': price_per_hour_range[1],
    })

    if request.method == 'POST':
        form = FindVenueForm(request.POST)
        # lower = request.POST.get('lower', '')
        # upper = request.POST.get('upper', '')

        if form.is_valid():
            search_location = form.cleaned_data['location']
            venue_type = form.cleaned_data['venue_type']
            # price_per_hour_range = [lower, upper]
            price_per_hour_range = [form.cleaned_data['price_per_hour_lower'],
                                    form.cleaned_data['price_per_hour_upper']]

    g = geocoder.google(search_location)
    search_geo = Point(float(g.lat), float(g.lng))

    pnt = GEOSGeometry(search_geo)
    venues = hmod.Listing.objects\
        .filter(geolocation__distance_lte=(pnt, D(mi=50)))\
        .filter(category__iexact=venue_type)\
        .filter(price_per_hour__gte=price_per_hour_range[0])\
        .filter(price_per_hour__lte=price_per_hour_range[1])\
        .filter(currently_listed=True)
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

        try:
            venue_locations_dict[venue.id] = {
                "lat": venue.geolocation.x,
                "lon": venue.geolocation.y,
                "title": venue.title
            }

        except:
            pass

    search_location = json.dumps(search_location)
    location_data = json.dumps(venue_locations_dict)  # lat and lon of venues
    price_per_hour_range = json.dumps(price_per_hour_range)

    context = {
        'form': form,
        'search_location': search_location,
        'venues': venues,
        'venue_pics_dict': venue_pics_dict,
        'location_data': location_data,
        'price_per_hour_range': price_per_hour_range,
    }
    return render_to_response('venue/venue_results.html', context, RequestContext(request))


PRICE_CHOICES = (
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('30', '30'),
    ('50', '50'),
    ('100', '100'),
)

class FindVenueForm(forms.Form):
    within_miles = forms.ChoiceField(required=False, widget=forms.Select(attrs={'id': 'venue-distance'}), label="Within", choices=choices.WITHIN_MILES_CHOICES)
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'location-search-autocomplete ui-autocomplete-input ui-corner-all'
    }))
    event_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    price_per_hour = forms.DecimalField(required=False, widget=forms.TextInput())
    price_per_hour_lower = forms.CharField(required=False)
    price_per_hour_upper = forms.CharField(required=False)