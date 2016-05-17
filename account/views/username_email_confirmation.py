from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone

def username_email_confirmation(request):
    '''the confirmation page when a user has requested to recover username OR has answered the security questions'''
    
    answered_or_not = request.GET.get('type')
                     
    context = {
        'answered_or_not': answered_or_not,
    }
    return render(request, 'account/username_email_confirmation.html', context)
    