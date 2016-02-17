from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from lib import forms as custom_forms
from lib import choices
from capstone.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import os.path

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login
@login_required
def calendar(request):
    '''select available dates for a venue'''
    
    form = Calendar_Form()

    if request.method == 'POST':
        form = Calendar_Form(request.POST)

        if form.is_valid():  
            return HttpResponseRedirect('/homepage/')

    context = {
        'form': form,
    }
    return render(request, 'venue/calendar.html', context)

# VENUE_FEATURE_CHOICES = choices.FEATURE_CHOICES

class Calendar_Form(forms.Form):
    dates_available = forms.CharField(widget=forms.TextInput())
    weekends = forms.BooleanField(required=False)
    