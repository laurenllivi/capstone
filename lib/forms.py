from django import forms
import os.path
from PIL import Image

def handle_uploaded_venue_file(file,listing_id,file_name):
    folder = ('static/images/venue-images/'+str(listing_id))
    if not os.path.exists(folder):
        os.makedirs(folder)
    destination = open(folder+'/'+file_name, 'wb+')
    
    # resize and optimize the photo before upload
    optimizedImage = Image.open(file)
    print(optimizedImage.size)
    
    for chunk in file.chunks():
        destination.write(chunk)
        
def handle_uploaded_profile_pic(file, user_id):
    folder = ('static/images/profile-images')
    if not os.path.exists(folder):
        os.makedirs(folder)
    destination = open(folder+'/'+file.name, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)