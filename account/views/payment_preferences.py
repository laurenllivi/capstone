from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms

@login_required
def payment_preferences(request):
    
    user = request.user
        
    context = {
        'user': user,

    }
    return render(request, 'account/payment_preferences.html', context)

