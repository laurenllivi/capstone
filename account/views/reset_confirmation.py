from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone

def reset_confirmation(request):
    '''the confirmation page when a user has reset password OR had a link sent to reset the password'''
    
    sent_or_reset = request.GET.get('type')
                     
    context = {
        'sent_or_reset': sent_or_reset,
    }
    return render(request, 'account/reset_confirmation.html', context)
    