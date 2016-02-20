from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone
from django.contrib.auth import authenticate

def message_home(request):
    ''' the messaging dashboard '''    
   
    context = {
        
    }
    return render(request, 'message/message_home.html', context)
