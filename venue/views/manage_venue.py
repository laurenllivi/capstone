from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from lib import forms as custom_forms
from lib import choices
from capstone.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import os.path
from django.contrib.gis.geos import Point
import geocoder

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login
@login_required
def manage_venue(request, listing_id):
    '''create new listing'''
    
    user = request.user
    
    # see if this is a new or existing venue
    new = request.GET.get('status')
    
    # if this is a new venue . . .
    if new is not None:
        form = NewVenueForm()
        imageForm = NewImageForm()
        listing = None
        newImage = None
        
    # it's an existing venue . . .    
    else:
        # create the venue form and prepopulate it with saved values
        listing = hmod.Listing.objects.get(id=listing_id)
        
        # make sure that only the owner of the venue can access this page
        # (since the venue ID is passed through the URL)
        if user.id != listing.user.id:
            return HttpResponseRedirect('/homepage/error_message')
        
        newImage = hmod.Listing_Photo()
        try:
            listing_features = hmod.Listing_Feature.objects.filter(feature_id=listing_id)
        except hmod.Listing_Feature.DoesNotExist:
            listing_features = None

        # location = geocoder.google([listing.geolocation.x, listing.geolocation.y], method='reverse')

        form = NewVenueForm(initial={
            'title': request.session.get('venueform_title') or listing.title,
            'category': listing.category,
            'sq_footage': listing.sq_footage,
            'num_guests': listing.num_guests,
            'description': listing.description,
            'parking_desc': listing.parking_desc,
            #can't figure out how to prepopulate with saved values
            'features': listing_features,
            'street': listing.street,
            'street2': listing.street2,
            'city': listing.city,
            'state': listing.state,
            'zipcode': listing.zipcode,
            'price_per_hour': listing.price_per_hour,
            'price_per_hour_weekend': listing.price_per_hour_weekend,

        })
        
        imageForm = NewImageForm()

    success = False

    if request.method == 'POST':
        # if it's a submit of the photos form, process ONLY that form
        if 'imagesForm' in request.POST:
            imageForm = NewImageForm(request.POST, request.FILES)
            if imageForm.is_valid():
                
                # if this is a new venue and this form is being submitted before the main form . . .
                # we need to create the venue object first
                if new is not None:
                    listing = hmod.Listing()
                    listing.user = user
                    listing.save()
                # if it's an existing venue . . .
                else:
                    listing = hmod.Listing.objects.get(id=listing_id)
                
                has_image = request.FILES.get('image', False)
                if has_image: 
                    custom_forms.handle_uploaded_venue_file(request.FILES['image'],listing.id)
                    newImage = hmod.Listing_Photo()
                    newImage.image_title = imageForm.cleaned_data['image_title']
                    newImage.image_name = imageForm.cleaned_data['image'].name   
                    newImage.image_file = "/static/images/venue-images/" + str(listing_id) + "/" + imageForm.cleaned_data['image'].name
                    newImage.listing = listing
                    newImage.save()
                    
                    # reset the url param to be the id of the venue
                    listing_id = listing.id
                    
                return HttpResponseRedirect('/venue/manage_venue/%s/' % listing.id)
                    
        # process the main form            
        elif 'mainForm' in request.POST:     
            form = NewVenueForm(request.POST)
            
            if form.is_valid():
                if new is not None:
                    listing = hmod.Listing()
                    newImage = hmod.Listing_Photo()
                  
                success = True
                listing.user = user
                listing.title = form.cleaned_data['title']
                listing.category = form.cleaned_data['category']
                listing.sq_footage = form.cleaned_data['sq_footage']
                listing.num_guests = form.cleaned_data['num_guests']
                listing.description = form.cleaned_data['description']
                listing.parking_desc = form.cleaned_data['parking_desc']
            
                feature_list = form.cleaned_data['features'].all()
                for feature in feature_list:
                    listing_feature = hmod.Listing_Feature()
                    listing_feature.listing = listing
                    listing_feature.feature = feature
                    listing_feature.save()
                
                listing.street = form.cleaned_data['street']
                listing.street2 = form.cleaned_data['street2']
                listing.city = form.cleaned_data['city']
                listing.state = form.cleaned_data['state']
                listing.zipcode = form.cleaned_data['zipcode']
                listing.price_per_hour = form.cleaned_data['price_per_hour']
                listing.price_per_hour_weekend = form.cleaned_data['price_per_hour_weekend']

                g = geocoder.google(
                    form.cleaned_data['street'] + " " +
                    form.cleaned_data['street2'] + ", " +
                    form.cleaned_data['city'] + ", " +
                    form.cleaned_data['state']
                )

                listing.geolocation = Point(float(g.lat), float(g.lng))
                listing.save()
            
                # reset the url param to be the id of the venue
                listing_id = listing.id

                return HttpResponseRedirect('/venue/manage_venue/%s/' % listing_id)

    # get the images for this listing
    images = hmod.Listing_Photo.objects.filter(listing=listing)

    # the equivalent of template_vars in DMP
    context = {
        'success': success,
        'form': form,
        'imageForm': imageForm,
        'images': images,
        'listing': listing,
    }
    return render(request, 'venue/manage_venue.html', context)

@login_required
def manage_venue__del_img(request, listing_id, image_id):   
    '''deleting an image from a venue listing'''
    
    user = request.user
    
    listing = hmod.Listing.objects.get(id=listing_id)
    image = hmod.Listing_Photo.objects.get(id=image_id)
    
    image.delete()
    
    # how do we actually delete the object? Do we even want to do that?
    
    return HttpResponseRedirect('/venue/manage_venue/%s/' % listing_id)

class NewVenueForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    sq_footage = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0)
    num_guests = forms.DecimalField(max_digits=6, decimal_places=0, min_value=0)
    description = forms.CharField(widget=forms.Textarea)
    parking_desc = forms.CharField(widget=forms.Textarea)
    features = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=hmod.Feature.objects.all(), required=False)
    search_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search for your address . . .',
        'id': 'autocomplete',
        'onFocus': 'geolocate()',
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'street_number'
    }))
    street2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'route'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'locality'
    }))
    state = forms.ChoiceField(choices=choices.STATE_CHOICES, widget=forms.Select(attrs={
        'id': 'administrative_area_level_1'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'postal_code'
    }))
    price_per_hour = forms.DecimalField(max_digits=6, decimal_places=0, min_value=0)
    price_per_hour_weekend = forms.DecimalField(max_digits=6, decimal_places=0, min_value=0)
    
class NewImageForm(forms.Form):
    image_title = forms.CharField(widget=forms.TextInput(), required=False)
    image = forms.ImageField(label='Select a file', required=False)
