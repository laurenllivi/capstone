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
def calendar(request, listing_id):
    '''select available dates for a venue'''
    
    # get the listing passed in the url
    listing = hmod.Listing.objects.get(id=listing_id)
    # get the listing_dates for this listing
    available_dates = hmod.Listing_Date.objects.filter(listing_id = listing.id)
    
    form = Calendar_Form(initial={
        # why isn't this working???
        'dates_available': available_dates,
    })

    if request.method == 'POST':
        form = Calendar_Form(request.POST)

        if form.is_valid():  
            # each date is saved as a new object in the Listing_Date model
            # split the string into individual dates to save  
            dates_string = form.cleaned_data['dates_available']
            dates_list = dates_string.split(', ')
            for date in dates_list: 
                # first rearrange the date to meet the datetime object python format
                correct_format_year = date.split("/")[2]
                correct_format_month = date.split("/")[0]
                correct_format_day = date.split("/")[1]
                correct_format_date = correct_format_year + "-" + correct_format_month + "-" + correct_format_day
                print(">>>>>>>>>>>>>>" + str(correct_format_date))
                
                # save to the database
                d = hmod.Listing_Date()
                d.date = correct_format_date
                d.listing = listing
                d.save()
            
            return HttpResponseRedirect('/venue/calendar')

    context = {
        'form': form,
    }
    return render(request, 'venue/calendar.html', context)

class Calendar_Form(forms.Form):
    dates_available = forms.CharField(widget=forms.TextInput(attrs={
        # 'disabled': 'disabled',
        'rows': '3',
        }))
    weekends = forms.BooleanField(required=False)
    
    def clean(self):
        if len(self.errors) == 0:
            return self.cleaned_data
        else:
            print(self.errors)
    