from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from capstone.settings import STATIC_URL as static_url

def new_user(request):
    '''create a new user'''
    
    # create the new user form
    form = New_User_Form()
    
    if request.method == 'POST':
        form = New_User_Form(request.POST)
        
        # if the form passes my clean methods . . .
        # also prevents SQL injection
        if form.is_valid():
            newUser = hmod.User()
            newUser.first_name = form.cleaned_data['first_name']
            newUser.last_name = form.cleaned_data['last_name']
            newUser.username = form.cleaned_data['username']
            newUser.set_password(form.cleaned_data['password'])
            newUser.email = form.cleaned_data['email']
            newUser.phone = form.cleaned_data['phone']
            newUser.save()
            
            newUserPhoto = hmod.User_Photo()
            newUserPhoto.image_name = newUser.username + "_profile_photo"
            newUserPhoto.image_title = newUser.username + "_profile_photo"
            newUserPhoto.image_file = static_url + "images/profile-images/default_user.png"
            newUserPhoto.save()
            
            newUser.profile_pic = newUserPhoto
            newUser.save()
            
            return HttpResponseRedirect('/account/profile')
            
    context = {
        'form' : form,
    }
    return render(request, 'account/new_user.html', context)
    
class New_User_Form(forms.Form):       
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label="Retype Password", widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())
    phone = forms.IntegerField(widget=forms.TextInput(), required=False)
 
    # checks to make sure that the username isn't already taken   
    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        try:
            hmod.User.objects.get(username = self.cleaned_data.get('username'))
            raise forms.ValidationError("That username is already taken. Please choose another.")
        except hmod.User.DoesNotExist:
            pass
        # then check to make sure the new password fields match
        if password1 != password2:
            raise forms.ValidationError('The passwords do not match')
        return self.cleaned_data