from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.contrib.auth.decorators import login_required

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login

@login_required
def manage_venue(request, listing_id):
    '''create new listing'''
    
    #authenticate the user
    #if not request.user.is_authenticated():
       #return HttpResponseRedirect('/account/login/')

    # create the new venue form
    listing = hmod.Listing.objects.get(id=listing_id)

    form = NewVenueForm(initial={
        'title': request.session.get('venueform_title') or listing.title,
        'category': listing.category,
        'description': listing.description,
        'street': listing.street,
        'street2': listing.street2,
        'city': listing.city,
        'state': listing.state,
        'zipcode': listing.zipcode,
    })

    if request.method == 'POST':
        form = NewVenueForm(request.POST)
        print ("method was post")

        if form.is_valid():
            listing.title = form.cleaned_data['title']
            listing.category = form.cleaned_data['category']
            listing.description = form.cleaned_data['description']
            listing.street = form.cleaned_data['street']
            listing.street2 = form.cleaned_data['street2']
            listing.city = form.cleaned_data['city']
            listing.state = form.cleaned_data['state']
            listing.zipcode = form.cleaned_data['zipcode']
            listing.save()
            print ("Form was valid")

            return HttpResponseRedirect('/venue/manage_venue/%s' % listing_id)

        print ("Form was NOT valid")

    # the equivalent of template_vars in DMP
    context = {
        'form': form,
    }
    return render(request, 'venue/manage_venue.html', context)

VENUE_TYPE_CHOICES = (
    ('backyard', 'Backyard'),
    ('barn', 'Barn'),
    ('porch', 'Deck/Porch/Patio'),
    ('theater', 'Home Theater'),
    ('pool', 'Pool'),
    ('rooftop', 'Rooftop'),
    ('sports', 'Sports')
)

VENUE_FEATURE_CHOICES = (
    ('garden', 'Garden'),
    ('gazebo', 'Gazebo'),
    ('jacuzzi', 'Jacuzzi'),
    ('lawn', 'Lawn'),
    ('playset', 'Playset'),
    ('pool', 'Pool'),
    ('water', 'Water Feature')
)

STATE_CHOICES = (
    ('AL', "Alabama"),
    ('CO', "Colorado"),
    ('ID', "Idaho"),
    ('TX', "Texas"),
    ('UT', "Utah"),
)


class NewVenueForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=VENUE_TYPE_CHOICES)
    description = forms.CharField(widget=forms.Textarea)
    features = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=VENUE_FEATURE_CHOICES, required=False)
    street = forms.CharField(widget=forms.TextInput)
    street2 = forms.CharField(widget=forms.TextInput)
    city = forms.CharField(widget=forms.TextInput())
    state = forms.ChoiceField(widget=forms.Select(), choices=STATE_CHOICES)
    zipcode = forms.CharField(widget=forms.TextInput)