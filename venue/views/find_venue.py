from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.contrib.auth.decorators import login_required

def find_venue(request):
    '''search for a venue'''
    
    form = Find_Venue()

    context = {
        'form': form,
    }
    return render(request, 'venue/find_venue.html', context)

WITHIN_MILES_CHOICES = (
    ('5', '5 miles'),
    ('10', '10 miles'),
    ('15', '15 miles'),
    ('20', '20 miles'),
    ('30', '30 miles'),
    ('50', '50 miles'),
    ('100', '100 miles +'),
    
)

VENUE_TYPE_CHOICES = (
    ('backyard', 'Backyard'),
    ('barn', 'Barn'),
    ('porch', 'Deck/Porch/Patio'),
    ('theater', 'Home Theater'),
    ('pool', 'Pool'),
    ('rooftop', 'Rooftop'),
    ('sports', 'Sports')
)

class Find_Venue(forms.Form):
    within_miles = forms.ChoiceField(widget=forms.Select(), label = "Within", choices=WITHIN_MILES_CHOICES)
    location = forms.CharField(widget=forms.TextInput())
    event_date = forms.CharField(widget=forms.TextInput())
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=VENUE_TYPE_CHOICES)
    