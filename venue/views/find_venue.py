from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from lib import choices
from homepage import models as hmod
from django.contrib.auth.decorators import login_required
import geocoder
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D #shortcut for distance
import simplejson as json

def find_venue(request):
    '''search for a venue'''

    pnt = GEOSGeometry('POINT(40.24 -111.66)')

    venues = hmod.Listing.objects.filter(geolocation__distance_lte=(pnt, D(mi=50)))
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

    location_data = json.dumps(venue_locations_dict)

    form = Find_Venue()

    context = {
        'form': form,
        'venues': venues,
        'venue_pics_dict': venue_pics_dict,
        'location_data': location_data
    }
    return render(request, 'venue/find_venue.html', context)

class Find_Venue(forms.Form):
    within_miles = forms.ChoiceField(widget=forms.Select(), label = "Within", choices=choices.WITHIN_MILES_CHOICES)
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'location-search-autocomplete ui-autocomplete-input ui-corner-all'
    }))
    event_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    price_per_hour = forms.DecimalField(widget=forms.TextInput())
    