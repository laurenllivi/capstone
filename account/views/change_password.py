from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone
from django.contrib.auth import authenticate

def change_password(request):
    '''changing a user's password - once they are already logged in'''
    
    user = request.user
    security_questions = hmod.User_Security_Question.objects.filter(user=user)
    
    form = Change_Password_Form()
    form2 = Change_Security_Questions_Form(initial={
        'security_question_1': security_questions[0].security_question,
        'security_answer_1': security_questions[0].answer,
        'security_question_2': security_questions[1].security_question,
        'security_answer_2': security_questions[1].answer
    })
    
    
    if request.method == 'POST': 
        if 'security_questions' in request.POST:
            form2 = Change_Security_Questions_Form(request.POST)
            if form2.is_valid():
                security_set_1 = hmod.User_Security_Question.objects.filter(user=user)[0]
                security_set_1.security_question = form2.cleaned_data['security_question_1']
                security_set_1.answer = form2.cleaned_data['security_answer_1']
                security_set_1.save()
            
                security_set_2 = hmod.User_Security_Question.objects.filter(user=user)[1]
                security_set_2.security_question = form2.cleaned_data['security_question_2']
                security_set_2.answer = form2.cleaned_data['security_answer_2']
                security_set_2.save()
                
                return HttpResponseRedirect('/account/change_password/')
                
        else:
            form = Change_Password_Form(request.POST, request=request)
        
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
            
                return HttpResponseRedirect("/account/profile/")                   
                
    context = {
        'form': form, 
        'form2': form2,
    }
    return render(request, 'account/change_password.html', context)
    
class Change_Password_Form(forms.Form): 
    # lets me access the request in the form
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Change_Password_Form, self).__init__(*args, **kwargs)
    
    current_password = forms.CharField(required=True, label="Old Password", widget=forms.PasswordInput())
    password = forms.CharField(required=True, label="New Password", widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm New Password", widget=forms.PasswordInput())
    
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
        
class Change_Security_Questions_Form(forms.Form):
    ''' allows the user to change the security questions '''
    security_question_1 = forms.ModelChoiceField(label="Security Question 1", queryset=hmod.Security_Question.objects.all(),initial=0)
    security_answer_1 = forms.CharField(label="Answer to Question 1", widget=forms.TextInput())
    security_question_2 = forms.ModelChoiceField(label="Security Question 2", queryset=hmod.Security_Question.objects.all())
    security_answer_2 = forms.CharField(label="Answer to Question 2",widget=forms.TextInput())