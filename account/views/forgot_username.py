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

def forgot_username(request):
    
    form = Forgot_Username_Form()
    
    if request.method == "POST": 
        
        form = Forgot_Username_Form(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # check to make sure the email entered is valid
            try:
                user = hmod.User.objects.get(email=email)
                # need to see if the query returns multiple users?
                # send the user an email with link to answer security questions
                
                email = user.email
                
                recovery_string = hmod.Recovery_String()
                recovery_string.rand_string = uuid4()
                recovery_string.expiration = timezone.now() + datetime.timedelta(hours=3)
                recovery_string.user = user
                recovery_string.save()
            
                url = "localhost:8000/account/answer_security_questions?string=" + str(recovery_string.rand_string)
            
                # send an email with reset link
                subject, from_email, to = 'Recover Username', settings.EMAIL_HOST_USER, email

                html_content = render_to_string('account/forgotUsernameTemplate.html', {'user':user, 'url': url})
                text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.mixed_subtype = 'related'
                msg.attach_alternative(html_content, "text/html")
                 
                msg.send()
                  
            except hmod.User.DoesNotExist:
                pass
                
            return HttpResponseRedirect("/account/username_email_confirmation?type=%s" %('not_answered'))       

    context = {
        'form': form,
    }
    return render(request, 'account/forgot_username.html', context)
    
class Forgot_Username_Form(forms.Form):  
    email = forms.EmailField(required=True, widget=forms.TextInput())
    
    # the email has to be unique when the user signs up, so we don't need a clean method here
    

