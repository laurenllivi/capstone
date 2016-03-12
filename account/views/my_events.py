from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from django.template.defaulttags import register

@login_required
def my_events(request):
    
    user = request.user
    
    # get approved events for the user
    approved_events = hmod.Rental_Request.objects.filter(user=user).filter(approved=True)
    pending_approval_events = hmod.Rental_Request.objects.filter(user=user).filter(approved=False)
        
    context = {
        'user': user,
        'approved_events': approved_events,
        'pending_approval_events': pending_approval_events,
        
    }
    return render(request, 'account/my_events.html', context)