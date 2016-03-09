from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms

@login_required
def my_reservations(request):
    
    user = request.user
    listings = hmod.Listing.objects.filter(user_id=user.id)
    venue_pics_dict = {}
    request_list = []

    for listing in listings:
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
            # and add it to the dictionary
            venue_pics_dict[listing.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass

        requests = hmod.Rental_Request.objects.filter(listing_id=listing.id)
        for i in requests:
            request_list.append(i)

    context = {
        'user': user,
        'request_list': request_list,
        'venue_pics_dict': venue_pics_dict,
    }

    return render(request, 'account/my_reservations.html', context)