from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from lib import forms as custom_forms
from capstone.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import os.path

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login
@login_required
def manage_venue(request, listing_id):
    '''create new listing'''

    # create the new venue form
    listing = hmod.Listing.objects.get(id=listing_id)
    newImage = hmod.Listing_Photo()

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

    success = False

    if request.method == 'POST':
        form = NewVenueForm(request.POST, request.FILES)

        if form.is_valid():
            success = True
            listing.title = form.cleaned_data['title']
            listing.category = form.cleaned_data['category']
            listing.description = form.cleaned_data['description']
            listing.street = form.cleaned_data['street']
            listing.street2 = form.cleaned_data['street2']
            listing.city = form.cleaned_data['city']
            listing.state = form.cleaned_data['state']
            listing.zipcode = form.cleaned_data['zipcode']
            listing.save()

            custom_forms.handle_uploaded_venue_file(request.FILES['image'],listing_id)
            newImage.image_title = form.cleaned_data['image_title']
            newImage.image_name = form.cleaned_data['image'].name

            newImage.listing = listing
            newImage.save()

            return HttpResponseRedirect('/venue/manage_venue/%s' % listing_id)

    images = hmod.Listing_Photo.objects.all()

    # the equivalent of template_vars in DMP
    context = {
        'success': success,
        'form': form,
        'images': images,
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

    image_title = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField(label='select a file', required=False)