from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from django.template.defaulttags import register

@login_required
def my_events(request):
    
    user = request.user
        
    context = {
        'user': user,
        
    }
    return render(request, 'account/my_events.html', context)