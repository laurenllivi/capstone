from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import datetime
from time import time
import decimal
import stripe

@login_required
def cc_info(request, rental_request_id):
    '''enter payment information'''
    
    user = request.user
    rental_request = hmod.Rental_Request.objects.get(id=rental_request_id)
    listing = hmod.Listing.objects.get(id=rental_request.listing.id)
    try:
        # get only the first pic from the venue
        venue_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
    except hmod.Listing_Photo.DoesNotExist:
        pass
    
    # need to get the listing_date to see whether to use weekend pricing or not
    listing_date = hmod.Listing_Date.objects.get(id=rental_request.listing_date.id)
    # weekday gets the day of the week, with 0 being Monday and 6 being Sunday
    weekday = listing_date.date.weekday()
    if weekday > 4:
        fee_base = listing.price_per_hour_weekend
        weekend = True
    else:
        fee_base = listing.price_per_hour
        weekend = False
        
    # then we need to subtract the end time from the start time to get the hours
    hours = rental_request.duration()
    # amount passed to stripe must be in cents
    fee = int((hours * fee_base) * 100)
    
    # for the template . . .
    fee_in_dollars = round(decimal.Decimal(fee / 100),2)
    
    context = {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        'user': user,
        'listing': listing,
        'rental_request': rental_request,
        'venue_pic': venue_pic,
        'listing_date': listing_date,
        'fee': fee,
        'weekend': weekend,
        'fee_in_dollars': fee_in_dollars,
    }
       
    # Process payment (via Stripe)
    
    if request.method == "POST":
        try:
            stripe_customer = user.charge(request, user.email, fee)
            # redirect to the success page
            return HttpResponseRedirect('/payment/success/%s/' % rental_request.id)
            
        except stripe.StripeError as se:
            error = se.args[0]
            context.update({'error': error})           
        
    return render(request, 'payment/cc_info.html', context)