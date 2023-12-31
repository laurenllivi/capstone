from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from localflavor.us.forms import USPhoneNumberField
from django.core.validators import validate_email

@login_required
def profile(request):
    
    user = request.user
    
    form = Edit_User_Form(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'bio': user.bio,
        # should we allow the user to change their password on this page?
    })
    
    if request.method == 'POST':
        form = Edit_User_Form(request.POST, request=request)
        
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.bio = form.cleaned_data['bio']
            user.save()
            
            # need to figure out how to send a success variable over so I can put a "success" message on the page
            
            return HttpResponseRedirect('/account/profile')
        
    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'account/profile.html', context)

class Edit_User_Form(forms.Form):
    
    # lets me access the request in the form
    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super(Edit_User_Form, self).__init__(*args, **kwargs)
    
    first_name = forms.CharField(max_length=50, widget=forms.TextInput())
    last_name = forms.CharField(max_length=50, widget=forms.TextInput())
    username = forms.CharField(max_length=20, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    phone = USPhoneNumberField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'xxx-xxx-xxxx'
    }))
    bio = forms.CharField(max_length=300, label="About Me", widget=forms.Textarea())

    # checks to make sure that the username isn't already taken   
    def clean_username(self):
        user = self.request.user
        if user.username == self.cleaned_data['username']:
            return self.cleaned_data['username']
        try:
            hmod.User.objects.get(username = self.cleaned_data['username'])
            raise forms.ValidationError("That username is already taken. Please choose another.")
        except hmod.User.DoesNotExist:
            pass
        return self.cleaned_data['username']
