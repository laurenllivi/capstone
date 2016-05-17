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
            
            newSecurityQuestion = hmod.User_Security_Question()
            newSecurityQuestion.user = newUser
            newSecurityQuestion.security_question = form.cleaned_data['security_question_1']
            newSecurityQuestion.answer = form.cleaned_data['security_answer_1']
            newSecurityQuestion.save()
            
            newSecurityQuestion2 = hmod.User_Security_Question()
            newSecurityQuestion2.user = newUser
            newSecurityQuestion2.security_question = form.cleaned_data['security_question_2']
            newSecurityQuestion2.answer = form.cleaned_data['security_answer_2']
            newSecurityQuestion2.save()
            
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
    security_question_1 = forms.ModelChoiceField(label="Security Question 1", queryset=hmod.Security_Question.objects.all(),initial=0)
    security_answer_1 = forms.CharField(label="Answer to Question 1", widget=forms.TextInput())
    security_question_2 = forms.ModelChoiceField(label="Security Question 2", queryset=hmod.Security_Question.objects.all())
    security_answer_2 = forms.CharField(label="Answer to Question 2",widget=forms.TextInput())
 
    # checks to make sure that the username or email isn't already taken  
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
            
        # check to make sure the username is unique
        try:
            hmod.User.objects.get(email = self.cleaned_data.get('email'))
            raise forms.ValidationError("That email is already registered with a user in our system. Please choose another.")
        except hmod.User.DoesNotExist:
            pass
            
        return self.cleaned_data