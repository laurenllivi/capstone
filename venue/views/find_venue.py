from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from lib import choices
from homepage import models as hmod
from django.contrib.auth.decorators import login_required
import geocoder
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D #shortcut for distance
import json as json


def find_venue(request):
    '''search for a venue'''

    search_location = 'Provo, Ut, United States'
    venue_type = 'Backyard'
    price_per_hour_range = [0, 5000]

    form = FindVenueForm()
    if request.method == 'POST':
        form = FindVenueForm(request.POST)
        if form.is_valid():
            search_location = form.cleaned_data['location']
            venue_type = form.cleaned_data['venue_type'].capitalize()
            price_per_hour_range = [form.cleaned_data['price_per_hour_lower'],
                                    form.cleaned_data['price_per_hour_upper']]
            print form.cleaned_data['price_per_hour_upper']

    g = geocoder.google(search_location)
    search_geo = Point(float(g.lat), float(g.lng))

    pnt = GEOSGeometry(search_geo)
    venues = hmod.Listing.objects\
        .filter(geolocation__distance_lte=(pnt, D(mi=50)))\
        .filter(listing_type=venue_type)
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
                "lon": venue.geolocation.y
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
    return render(request, 'venue/find_venue.html', context)


class FindVenueForm(forms.Form):
    within_miles = forms.ChoiceField(required=False, widget=forms.Select(), label = "Within", choices=choices.WITHIN_MILES_CHOICES)
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'location-search-autocomplete ui-autocomplete-input ui-corner-all'
    }))
    event_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    price_per_hour = forms.DecimalField(required=False, widget=forms.TextInput())
    price_per_hour_lower = forms.DecimalField(required=False)
    price_per_hour_upper = forms.DecimalField(required=False)