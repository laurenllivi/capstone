from django import forms
import os.path

def handle_uploaded_venue_file(file,listing_id):
    folder = ('static/images/venue-images/'+listing_id)
    if not os.path.exists(folder):
        os.makedirs(folder)
    destination = open(folder+'/'+file.name, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)