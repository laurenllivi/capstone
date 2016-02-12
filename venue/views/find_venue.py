from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from lib import choices
from homepage import models as hmod
from django.contrib.auth.decorators import login_required

def find_venue(request):
    '''search for a venue'''
    
    form = Find_Venue()

    context = {
        'form': form,
    }
    return render(request, 'venue/find_venue.html', context)

class Find_Venue(forms.Form):
    within_miles = forms.ChoiceField(widget=forms.Select(), label = "Within", choices=choices.WITHIN_MILES_CHOICES)
    location = forms.CharField(widget=forms.TextInput())
    event_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    venue_type = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    price_per_hour = forms.DecimalField(widget=forms.TextInput())
    