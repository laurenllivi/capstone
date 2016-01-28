from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from uuid import *
from django.core.mail import send_mail
from django.utils import timezone
import datetime
from capstone import settings as settings

def forgot_password(request):
    
    form = Forgot_Password_Form()
    
    if request.method == "POST": 
        
        form = Forgot_Password_Form(request.POST)
        
        if form.is_valid():
        
            username = form.cleaned_data['username']
            user = hmod.User.objects.get(username= username)
            email = user.email
            recovery_string = hmod.Recovery_String()
            recovery_string.rand_string = uuid4()
            recovery_string.expiration = timezone.now() + datetime.timedelta(hours=3)
            recovery_string.user = user
            recovery_string.save()
            user.save()
            
            url = "localhost:8000/account/reset_password/?string=" + str(recovery_string.rand_string)
        
            subject = "Forgotten Password"
            message = "Please click the link below to be taken to a reset password page.\n\n" + url
            from_email = settings.EMAIL_HOST_USER
            to_list = [ email ]

            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            #return HttpResponseRedirect('/account/reset_confirmation')
            return HttpResponseRedirect("/account/reset_confirmation/?type=%s" %('sent'))

    context = {
        'form': form,
    }
    return render(request, 'account/forgot_password.html', context)
    
class Forgot_Password_Form(forms.Form):
    
    username = forms.CharField(required=True, widget=forms.TextInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            hmod.User.objects.get(username=username)
            return username
        except hmod.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

