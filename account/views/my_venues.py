from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms

@login_required
def my_venues(request):
    
    user = request.user
    my_venues = hmod.Listing.objects.filter(user=user)
        
    context = {
        'user': user,
        'my_venues': my_venues,
        
    }
    return render(request, 'account/my_venues.html', context)