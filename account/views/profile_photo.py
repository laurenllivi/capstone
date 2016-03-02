from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from lib import forms as custom_forms
from capstone.settings import MEDIA_ROOT
from capstone.settings import STATIC_URL as static_url
import os.path

@login_required
def profile_photo(request):
    
    user = request.user
    
    # create the form 
    photo_upload_form = New_Profile_Photo_Form()
    
    if request.method == 'POST':
        photo_upload_form = New_Profile_Photo_Form(request.POST, request.FILES)
            
        if photo_upload_form.is_valid():
            has_image = request.FILES.get('image', False)
            if has_image:
                # actually write the contents of the file to the directory
                custom_forms.handle_uploaded_profile_pic(request.FILES['image'],user.id)
                # change the photo attributes in the database
                user.profile_pic.image_name =  photo_upload_form.cleaned_data['image'].name
                user.profile_pic.image_title = photo_upload_form.cleaned_data['image'].name
                user.profile_pic.image_file = static_url + "images/profile-images/" + photo_upload_form.cleaned_data['image'].name
                user.profile_pic.save()
        
        
    context = {
        'user': user,
        'photo_upload_form': photo_upload_form,

    }
    return render(request, 'account/profile_photo.html', context)
    
@login_required
def profile_photo__del_img(request):   
    '''deleting a user's profile image'''
    
    user = request.user
    user_photo = user.profile_pic
    user_photo.image_name = user.username + "_profile_photo"
    user_photo.image_title = user.username + "_ profile_photo"
    user_photo.image_file = static_url + "images/profile-images/default_user.png"
    user_photo.save()
        
    return HttpResponseRedirect('/account/profile_photo/')
    
class New_Profile_Photo_Form(forms.Form):
    image = forms.ImageField(label="Change your profile photo",required=False)
    

