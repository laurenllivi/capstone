from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required
def success(request, rental_request_id):
    '''the user's payment was successful'''
    
    user = request.user
    rental_request = hmod.Rental_Request.objects.get(id=rental_request_id)
    listing = hmod.Listing.objects.get(id=rental_request.listing.id)
    listing_date = hmod.Listing_Date.objects.get(id=rental_request.listing_date.id)
    listing_policy = hmod.Listing_Policy.objects.get(listing_id=listing.id)
    cancellation_policy = hmod.Cancellation_Policy.objects.get(id=listing_policy.cancellation_policy_id)    
    
    context = {
       'user': user,
       'listing': listing,
       'rental_request': rental_request,
       'cancellation_policy': cancellation_policy,
       'listing_date': listing_date,
    }       

    return render(request, 'payment/success.html', context)