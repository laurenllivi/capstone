from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from django.forms.utils import ErrorList
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
from pytz import timezone
from tzwhere import tzwhere
from django.conf import settings
from django.template.defaultfilters import filesizeformat 

# make sure the user is logged in before accessing this view
# redirects the user to the previous url after login
@login_required
def manage_venue(request, listing_id):
    '''create new listing'''

    user = request.user
    features = []
    tab = request.GET.get('tab', '1')
    policies = hmod.Cancellation_Policy.objects.all()

    # see if this is a new or existing venue
    new = request.GET.get('status')
    
    # if this is a new venue . . .
    if new is not None:
        form = NewVenueForm()
        imageForm = NewImageForm()
        calendarForm = CalendarForm()
        dates_list_string = ""
        dates_available = ""
        listing = None
        newImage = None
        cancellation_policy = hmod.Listing_Policy.objects.filter().first()
        
    # it's an existing venue . . .    
    else:
        # create the venue form and prepopulate it with saved values
        listing = hmod.Listing.objects.get(id=listing_id)
        available_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id)
        cancellation_policy = hmod.Listing_Policy.objects.filter(listing_id=listing.id).first()

        # make sure that only the owner of the venue can access this page
        # (since the venue ID is passed through the URL)
        if user.id != listing.user.id:
            return HttpResponseRedirect('/homepage/error_message')
        
        newImage = hmod.Listing_Photo()
        try:
            listing_features = hmod.Listing_Feature.objects.filter(listing_id=listing_id)
            for feature in listing_features:
                #add feature names to list to prepopulate checkboxes
                features.append(hmod.Feature.objects.get(id=feature.feature_id).name)
        except hmod.Listing_Feature.DoesNotExist:
            listing_features = None

        # use my custom method to convert the list of objects into a string of dates
        dates_available = convert_date.convert_db_into_date_string(available_dates)
                
        calendarForm = CalendarForm(initial={
            'saved_dates': dates_available,
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
                    set_cancellation_policy(request, listing)
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
                    set_cancellation_policy(request, listing)
                    
                # it's an existing venue . . .
                else:
                    listing = hmod.Listing.objects.get(id=listing_id)
                    
                # each date is saved as a new object in the Listing_Date model
                # split the string into individual dates to save  
                dates_string = calendarForm.cleaned_data['dates_available']
                all_dates = hmod.Listing_Date.objects.filter(listing_id=listing.id)

                # if the user has submitted dates . . .
                if dates_string != "":
                    dates_list = dates_string.split(', ')
                    for date in dates_list:      
                        db_format_date = convert_date.convert_date_string_into_db(date)
                        # save to the database (if the same date isn't already in there)
                        try:
                            hmod.Listing_Date.objects.get(listing=listing, date=db_format_date)
                        except hmod.Listing_Date.DoesNotExist: 
                            d = hmod.Listing_Date()
                            d.date = db_format_date
                            d.listing = listing
                            d.save()
                            
                # take out the dates that are no longer selected
                for date in all_dates:
                    date_string = date.date.strftime('%m/%d/%Y')
                    if date_string not in dates_string:
                        date.delete()
                    
                    # reset the url param to be the id of the venue
                    listing_id = listing.id
                
            return HttpResponseRedirect('/venue/manage_venue/%s/' % listing.id)
                    
        # process the main form
        #################### Main Form (values aren't required ), Post Venue (values ARE required )################
        else:
            if 'postVenue' in request.POST:
                # make all fields required in order to post a venue
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
                form.fields['deposit'].required = required
                
                # make at least one image required
                image_count = hmod.Listing_Photo.objects.filter(listing_id=listing_id).count()
                if image_count == 0:
                    form.add_error(None, "You must add at least one venue photo")
                    
                # make at least one available date required
                date_count = hmod.Listing_Date.objects.filter(listing_id=listing_id).count()
                if date_count == 0:
                    form.add_error(None, "You must add at least one available date")
                
            elif 'mainForm' in request.POST:     
                form = NewVenueForm(request.POST)  
                # and fields are NOT required by default
                  
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
                listing.save()

                #save listing features
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

                set_cancellation_policy(request, listing)

                g = geocoder.google(
                    form.cleaned_data['street'] + " " +
                    form.cleaned_data['street2'] + ", " +
                    form.cleaned_data['city'] + ", " +
                    form.cleaned_data['state']
                )

                listing.geolocation = Point(float(g.lat), float(g.lng))
                tz = tzwhere.tzwhere()
                listing.timezone = tz.tzNameAt(listing.geolocation.x, listing.geolocation.y)
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
        'tab': tab,
        'dates_available': dates_available,
        'policies': policies,
        'cancellation_policy': cancellation_policy,
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

def set_cancellation_policy(request, listing):
     #set the cancellation policy
    print("Saving cancellation policy")
    try:
        updated_policy = request.POST['policy-select']
    except Exception:
        updated_policy = 2

    if hmod.Listing_Policy.objects.filter(listing_id=listing.id).exists():
        listing_policy = hmod.Listing_Policy.objects.filter(listing_id=listing.id)[0]
    else:
        listing_policy = hmod.Listing_Policy()
        listing_policy.listing_id = listing.id

    listing_policy.cancellation_policy_id = updated_policy
    listing_policy.save()

    return None


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
    cancellation_policy = forms.ModelChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        queryset=hmod.Cancellation_Policy.objects.all(),
        empty_label=None
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
    
    def clean_image(self):
        image = self.cleaned_data.get('image',False)
        if image:
            if image._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please choose an image that is smaller than 2.5 megabytes.")
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image.")
    
    # def clean(self):
#         '''ensure that the image is < 5 MB and is an image file type'''
#         content = self.cleaned_data['image']
#         if str(content._size) > settings.MAX_UPLOAD_SIZE:
#             print(">>>>>>>>>>>")
#             print("This photo is too large")
#             raise forms.ValidationError({'image_title': ['File is too large. Please upload a photo smaller than 5 megabytes.']})
#
#             # old - I think Django's image field validates the file type automatically
#             # if content_type in settings.CONTENT_TYPES:
#             #     print(">>>>>>>>>>>>")
#             #     print("yes, this is an image")
#             #     if str(content._size) > settings.MAX_UPLOAD_SIZE:
#             #         print(">>>>>>>>>>>")
#             #         print("This photo is too large")
#             #         raise forms.ValidationError({'image_title': ['File is too large. Please upload a photo smaller than 5 megabytes.']})
#             #
#             # else:
#             #     raise forms.ValidationError({'image_title': ['File type is not supported.']})
#             #     print(">>>>>>>>>>>>")
#             #     print("no, not an image")
#
#         return self.cleaned_data
    
class CalendarForm(forms.Form):
    saved_dates = forms.CharField(label="Test Saved Dates", required=False, widget=forms.TextInput(attrs={}))
    dates_available = forms.CharField(label="Saved Dates", required=False, widget=forms.TextInput(attrs={
        'readonly': 'true',
        }))
    
    def clean(self):
        if len(self.errors) == 0:
            return self.cleaned_data
        else:
            print(">>>>>>>>>>>>>>> You have errors >>>>>>>>>>>>")
            print(self.errors)
            
def manage_venue__del_venue(request, listing_id):
    '''deleting a user's venue - we are not really deleting. Just inactivating'''
    
    venue_to_delete = hmod.Listing.objects.get(id=listing_id)
    venue_to_delete.is_active = False
    venue_to_delete.save()
    
    return HttpResponseRedirect('/account/my_venues/')
