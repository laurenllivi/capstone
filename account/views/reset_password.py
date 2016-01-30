from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone

def reset_password(request):
    '''resetting a user's password'''
    
    todays_date = timezone.now()
    form = Reset_Password_Form()
    # grab the random string from the url params - identifies the user
    reset_password_key = request.GET.get('string')
    rand_string_object = hmod.Recovery_String.objects.get(rand_string=reset_password_key)
    user = hmod.User.objects.get(id=rand_string_object.user.id)
    key_expiration = rand_string_object.expiration
    
    if request.method == 'POST': 
        form = Reset_Password_Form(request.POST)
        
        if form.is_valid():
            if key_expiration <= todays_date:
                print(str(key_exp))
                raise forms.ValidationError("Your key has expired.")
            
            else:
                user.set_password(form.cleaned_data['password'])
                user.save()
                 
                # need to set the key values to null for the next time??
            
            return HttpResponseRedirect("/account/reset_confirmation")                   
                
    context = {
        'form': form, 
    }
    return render(request, 'account/reset_password.html', context)
    
class Reset_Password_Form(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput())
    
    def clean(self):
        
        if len(self.errors) == 0:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('The passwords do not match.')
        return self.cleaned_data