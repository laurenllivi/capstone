from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from lib import forms as custom_forms
from lib import choices
from capstone.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import os.path

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login
@login_required
def manage_venue(request, listing_id=0):
    '''create new listing'''
    
    user = request.user
    
    # see if this is a new or existing venue
    new = request.GET.get('status')
    
    # if this is an existing venue . . .
    if new is not None:
        listing = hmod.Listing()
        newImage = hmod.Listing_Photo()
        
        form = NewVenueForm()
        
    # it's an existing venue . . .    
    else:
        # create the new venue form
        listing = hmod.Listing.objects.get(id=listing_id)
        newImage = hmod.Listing_Photo()
        listing_features = hmod.Listing_Feature.objects.get(feature_id=listing_id)

        form = NewVenueForm(initial={
            'title': request.session.get('venueform_title') or listing.title,
            'category': listing.category,
            'sq_footage': listing.sq_footage,
            'num_guests': listing.num_guests,
            'description': listing.description,
            'parking_desc': listing.parking_desc,
            'street': listing.street,
            'street2': listing.street2,
            'city': listing.city,
            'state': listing.state,
            'zipcode': listing.zipcode,
            'price_per_hour': listing.price_per_hour,
            'price_per_hour_weekend': listing.price_per_hour_weekend
        })

    success = False

    if request.method == 'POST':
        form = NewVenueForm(request.POST, request.FILES)

        if form.is_valid():        
            success = True
            listing.user = user
            listing.title = form.cleaned_data['title']
            listing.category = form.cleaned_data['category']
            listing.sq_footage = form.cleaned_data['sq_footage']
            listing.num_guests = form.cleaned_data['num_guests']
            listing.description = form.cleaned_data['description']
            listing.parking_desc = form.cleaned_data['parking_desc']
            'this part is not working'
            feature_list = form.cleaned_data['features'].all()
            for feature in feature_list:
                listing.features.add(feature)
            listing.street = form.cleaned_data['street']
            listing.street2 = form.cleaned_data['street2']
            listing.city = form.cleaned_data['city']
            listing.state = form.cleaned_data['state']
            listing.zipcode = form.cleaned_data['zipcode']
            listing.price_per_hour = form.cleaned_data['price_per_hour']
            listing.price_per_hour_weekend = form.cleaned_data['price_per_hour_weekend']
            listing.save()
            
            # reset the url param to be the id of the venue
            listing_id = listing.id

            has_image = request.FILES.get('image', False)
            if has_image:
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

# VENUE_FEATURE_CHOICES = choices.FEATURE_CHOICES

class NewVenueForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=VENUE_TYPE_CHOICES)
    sq_footage = forms.DecimalField(max_digits=8, decimal_places=2)
    num_guests = forms.DecimalField(max_digits=6, decimal_places=0)
    description = forms.CharField(widget=forms.Textarea)
    parking_desc = forms.CharField(widget=forms.Textarea)
    features = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=hmod.Feature.objects.all(), required=False)
    street = forms.CharField(widget=forms.TextInput)
    street2 = forms.CharField(widget=forms.TextInput)
    city = forms.CharField(widget=forms.TextInput())
    state = forms.ChoiceField(widget=forms.Select(), choices=choices.STATE_CHOICES)
    zipcode = forms.CharField(widget=forms.TextInput)

    image_title = forms.CharField(widget=forms.TextInput(), required=False)
    image = forms.ImageField(label='select a file', required=False)

    price_per_hour = forms.DecimalField(max_digits=6, decimal_places=0)
    price_per_hour_weekend = forms.DecimalField(max_digits=6, decimal_places=0)

class ImageForm(forms.Form):
    image_title = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField(label='select a file', required=False)