from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from lib import choices
from django import forms

def index(request):
    
    form = Homepage_Search_Form()
    
        
    # the equivalent of template_vars in DMP
    context = {
        'form': form,
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/index.html', context)
    
class Homepage_Search_Form(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'index-search-field',
        'placeholder': 'Where is your event?',
    }))
    category = forms.ChoiceField(choices=choices.VENUE_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'index-search-field',
        'placeholder': 'Select a category'
    }))



