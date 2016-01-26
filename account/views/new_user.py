from django.http import HttpResponse
from django.shortcuts import render
from django import forms

def new_user(request):
    '''create a new user'''
    
    # create the new user form
    form = New_User_Form()
    
    # the equivalent of template_vars in DMP
    context = {
        'form' : form,
    }
    return render(request, 'account/new_user.html', context)
    
class New_User_Form(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.TextInput())
    phone = forms.IntegerField(widget=forms.TextInput())
    
    # Not sure if we need this
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(New_User_Form, self).__init__(*args, **kwargs)
 
    # checks to make sure that the username isn't already taken   
    # We will probably need this eventually as well 
    # def clean_username(self):
    #
    #     if self.request.urlparams[0] == 'new':
    #         try:
    #             smod.User.objects.get(username = self.cleaned_data['username'])
    #             raise forms.ValidationError("That username is already taken. Please choose another.")
    #         except smod.User.DoesNotExist:
    #             pass
    #         return self.cleaned_data['username']
    #     else:
    #         current_user = smod.User.objects.get(id = self.request.urlparams[0])
    #         if current_user.username == self.cleaned_data['username']:
    #             return self.cleaned_data['username']
    #         else:
    #             try:
    #                 smod.User.objects.get(username = self.cleaned_data['username'])
    #                 raise forms.ValidationError("That username is already taken. Please choose another.")
    #             except smod.User.DoesNotExist:
    #                 pass
    #             return self.cleaned_data['username']