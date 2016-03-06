from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from django.forms.util import ErrorList
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from homepage import models as hmod
from lib import forms as custom_forms
from lib import choices
from lib import convert_date_string as convert_date
from capstone.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
import os.path
from django.contrib.gis.geos import Point
import geocoder
from localflavor.us.forms import USZipCodeField
import uuid

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
        calendarForm = CalendarForm()
        dates_list_string = ""
        listing = None
        newImage = None
        
    # it's an existing venue . . .    
    else:
        # create the venue form and prepopulate it with saved values
        listing = hmod.Listing.objects.get(id=listing_id)
        available_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id)
        
        # make sure that only the owner of the venue can access this page
        # (since the venue ID is passed through the URL)
        if user.id != listing.user.id:
            return HttpResponseRedirect('/homepage/error_message')
        
        newImage = hmod.Listing_Photo()
        try:
            listing_features = hmod.Listing_Feature.objects.filter(listing_id=listing_id)
            features = []
            for feature in listing_features:
                #add feature names to list to prepopulate checkboxes
                features.append(hmod.Feature.objects.get(id=feature.feature_id).name)
        except hmod.Listing_Feature.DoesNotExist:
            listing_features = None

        # use my custom method to convert the list of objects into a string of dates
        dates_available = convert_date.convert_db_into_date_string(available_dates)
                
        calendarForm = CalendarForm(initial={
            'dates_available': dates_available,
        })

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
            'price_per_hour_weekend': listing.price_per_hour_weekend,
            'deposit': listing.deposit,

        })
        
        imageForm = NewImageForm()

    success = False

    if request.method == 'POST':
        # if it's a submit of the photos form, process ONLY that form
        ############################### Images Form ##############################################
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
                    newImage = hmod.Listing_Photo()
                    newImage.image_title = imageForm.cleaned_data['image_title']
                    newImage.image_name = str(uuid.uuid4()) + '.jpg'
                    # newImage.image_name = imageForm.cleaned_data['image'].name
                    newImage.image_file = "/static/images/venue-images/" + str(listing_id) + "/" + newImage.image_name
                    newImage.listing = listing
                    newImage.save()

                    custom_forms.handle_uploaded_venue_file(request.FILES['image'],listing.id, newImage.image_name)
                    # reset the url param to be the id of the venue
                    listing_id = listing.id
                    
                return HttpResponseRedirect('/venue/manage_venue/%s/' % listing.id)
            
        # process the calendar form
        ############################### Calendar Form ##############################################
        elif 'calendarForm' in request.POST:
            calendarForm = CalendarForm(request.POST)
            if calendarForm.is_valid():
                
                # if this is a new venue and this form is being submitted before the main form . . .
                # we need to create the venue object first
                if new is not None:
                    listing = hmod.Listing()
                    listing.user = user
                    listing.save()
                    
                # it's an existing venue . . .
                else:
                    listing = hmod.Listing.objects.get(id=listing_id)
                    
                # each date is saved as a new object in the Listing_Date model
                # split the string into individual dates to save  
                dates_string = calendarForm.cleaned_data['dates_available']
              
                # if the user has submitted dates . . .
                if dates_string != "":
                    dates_list = dates_string.split(', ')
                    for date in dates_list:      
                        db_format_date = convert_date.convert_date_string_into_db(date)
                        # save to the database (if the same date isn't already in there)
                        try:
                            hmod.Listing_Date.objects.get(listing=listing, date = db_format_date)
                        except hmod.Listing_Date.DoesNotExist: 
                            d = hmod.Listing_Date()
                            d.date = db_format_date
                            d.listing = listing
                            d.save()
                    
                    # reset the url param to be the id of the venue
                    listing_id = listing.id
                
            return HttpResponseRedirect('/venue/manage_venue/%s/' % listing.id)
                    
        # process the main form
        #################### Main Form (values aren't required ), Post Venue (values ARE required )################
        else:
            if 'postVenue' in request.POST:
                form = NewVenueForm(request.POST)
                required = 'postVenue' in request.POST
                form.fields['title'].required = required
                form.fields['category'].required = required
                form.fields['sq_footage'].required = required
                form.fields['num_guests'].required = required
                form.fields['description'].required = required
                form.fields['parking_desc'].required = required
                form.fields['street'].required = required
                form.fields['city'].required = required
                form.fields['state'].required = required
                form.fields['zipcode'].required = required
                form.fields['price_per_hour'].required = required
                form.fields['price_per_hour_weekend'].required = required
                
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

                all_features = hmod.Feature.objects.all()
                updated_feature_list = form.cleaned_data['features'].all()
                for feature in all_features:
                    if feature in updated_feature_list:
                        # if the feature is in the list of selected features, add to db
                        hmod.Listing_Feature.objects.update_or_create(
                            listing_id=listing.id, feature_id=feature.id
                        )
                    else:
                        # if feature is not in list of selected features, remove from db if it exists
                        if hmod.Listing_Feature.objects.filter(listing_id=listing.id, feature_id=feature.id).exists():
                                hmod.Listing_Feature.objects.filter(
                                    listing_id=listing.id, feature_id=feature.id
                                ).delete()



                listing.street = form.cleaned_data['street']
                listing.street2 = form.cleaned_data['street2']
                listing.city = form.cleaned_data['city']
                listing.state = form.cleaned_data['state']
                listing.zipcode = form.cleaned_data['zipcode']
                listing.price_per_hour = form.cleaned_data['price_per_hour']
                listing.price_per_hour_weekend = form.cleaned_data['price_per_hour_weekend']
                listing.deposit = form.cleaned_data['deposit']

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

                if 'mainForm' in request.POST:
                    return HttpResponseRedirect('/venue/manage_venue/%s/' % listing_id)
                elif 'postVenue' in request.POST:
                    return HttpResponseRedirect('/venue/post_venue/%s' % listing_id)

    # get the images for this listing
    images = hmod.Listing_Photo.objects.filter(listing=listing)

    # the equivalent of template_vars in DMP
    context = {
        'success': success,
        'form': form,
        'imageForm': imageForm,
        'calendarForm': calendarForm,
        'images': images,
        'listing': listing,
        'features': features,
        #'available_dates': available_dates,
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
    title = forms.CharField(required=False, max_length=100, widget=forms.TextInput())
    category = forms.ChoiceField(required=False, widget=forms.Select(), choices=choices.VENUE_TYPE_CHOICES)
    sq_footage = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    num_guests = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    description = forms.CharField(required=False, max_length=800, widget=forms.Textarea)
    parking_desc = forms.CharField(required=False, max_length=800, widget=forms.Textarea)
    features = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=hmod.Feature.objects.all()
    )
    search_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search for your address . . .',
        'id': 'autocomplete',
        'onFocus': 'geolocate()',
    }))
    street = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'id': 'street_number'
    }))
    street2 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'id': 'route'
    }))
    city = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'id': 'locality'
    }))
    state = forms.ChoiceField(
        required=False,
        choices=choices.STATE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'administrative_area_level_1'
        })
    )
    zipcode = USZipCodeField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'id': 'postal_code'
    }))
    price_per_hour = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    price_per_hour_weekend = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    deposit = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    def clean(self):
        if len(self.errors) == 0:
            return self.cleaned_data
        else:
            print(">>>>>>>>>>>>>>> You have errors >>>>>>>>>>>>")
            print(self.errors)
    
class NewImageForm(forms.Form):
    image_title = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    image = forms.ImageField(label='Select a file')

    # def clean(self):
    #     cleaned_data = super(NewImageForm, self).clean()
    #     if cleaned_data.get("image"):
    #         image_name = cleaned_data.get("image").name
    #
    #         if len(image_name) > 50:
    #             self.add_error('image', 'File name is too long')
    #             print(self.errors)
    #             print(">>>>>>>>>>>>>>>>>Added Image Errors>>>>>>>>>>>>>>>>>>>>>>>>")
    
class CalendarForm(forms.Form):
    dates_available = forms.CharField(label="Saved Dates", required=False, widget=forms.TextInput(attrs={
        # 'disabled': 'disabled',
        'readonly': 'true',
        }))
    
    def clean(self):
        if len(self.errors) == 0:
            return self.cleaned_data
        else:
            print(">>>>>>>>>>>>>>> You have errors >>>>>>>>>>>>")
            print(self.errors)
            
def process_request__del_venue(request, listing_id):
    '''deleting a user's venue - we are not really deleting. Just inactivating'''
    
    return HttpResponseRedirect('/account/my_venues/')
