from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone
from django.contrib.auth import authenticate

def change_password(request):
    '''changing a user's password - once they are already logged in'''
    
    form = Change_Password_Form()
    user = request.user
    
    if request.method == 'POST': 
        form = Change_Password_Form(request.POST, request=request)
        
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            return HttpResponseRedirect("/account/profile/")                   
                
    context = {
        'form': form, 
    }
    return render(request, 'account/change_password.html', context)
    
class Change_Password_Form(forms.Form):
    
    # lets me access the request in the form
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Change_Password_Form, self).__init__(*args, **kwargs)
    
    current_password = forms.CharField(required=True, label="Current Password", widget=forms.PasswordInput())
    password = forms.CharField(required=True, label="New Password", widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput())
    
    def clean(self):
        logged_in_user = self.request.user
        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('password', None)
        user = authenticate(username=logged_in_user.username, password=current_password)
        
        # if there are no other form errors . . .
        if len(self.errors) == 0:
            # first check to make sure the user entered the correct current password
            if user == None:            
                raise forms.ValidationError("Your current password is incorrect")   
            # then check to make sure the new password fields match    
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('The passwords do not match')
        return self.cleaned_data