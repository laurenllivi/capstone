from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.contrib.auth import logout as logout_auth

def logout(request):
    '''log the user out if they are not authenticated'''
                       
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect('/account/login/')  
          
    else: 
        
        logout_auth(request)
        
        return HttpResponseRedirect('/homepage/')
    
