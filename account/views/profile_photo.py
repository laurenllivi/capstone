from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms

@login_required
def profile_photo(request):
    
    user = request.user
        
    context = {
        'user': user,

    }
    return render(request, 'account/profile_photo.html', context)

