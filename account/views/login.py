from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def login(request):
    
    form = Login_Form()
    
    if request.method == 'POST': 
        form = Login_Form(request.POST)
        
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            #get the 'next' variable if there is one
            next_page = request.GET.get('next')
           
            # user is not none if the username exists in the database
            if user is not None:            
                auth_login(request, user)
                
                # if the user arrived at this page anywhere other than clicking "login," they will be redirected to the previous page upon successful login
                if next_page is not None:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponse('<script> window.location.href="/account/profile";</script>')
            
            else:
                # the authentication system was unable to verify the username and password
                print("Invalid username or password")
                return HttpResponse('<script> window.location.href="/account/login/";</script>')                
                
    context = {
        'form': form, 
    }
    return render(request, 'account/login.html', context)
    
class Login_Form(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self): 
        user = None
        if len(self.errors) ==0:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user == None:            
            raise forms.ValidationError("Bad username or password")
