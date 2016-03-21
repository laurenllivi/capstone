from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from uuid import *
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
            
            # send an email with reset link
            subject, from_email, to = 'Reset Your Password', settings.EMAIL_HOST_USER, email

            html_content = render_to_string('account/forgotPWTemplate.html', {'user':user, 'url': url})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.mixed_subtype = 'related'
            msg.attach_alternative(html_content, "text/html")
                 
            msg.send()
            
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

