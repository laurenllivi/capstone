from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from lib import choices
from django import forms

def index(request):
    
    form = Homepage_Search_Form()
    
    if request.method == 'POST':
        form = Homepage_Search_Form(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            category = form.cleaned_data['category']
            # now what to do with these . . .    
            return HttpResponseRedirect('/venue/find_venue/' + str(city) + '/' + str(category))
            
    # the equivalent of template_vars in DMP
    context = {
        'form': form,
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/index.html', context)
    
class Homepage_Search_Form(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'index-search-field ui-autocomplete-input ui-corner-all location-search-autocomplete',
        'placeholder': 'Where is your event?',
    }))
    category = forms.ChoiceField(choices=choices.VENUE_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'index-search-field',
        'placeholder': 'Select a category'
    }))



