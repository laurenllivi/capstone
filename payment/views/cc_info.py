from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import datetime
import stripe

@login_required
def cc_info(request, rental_request_id):
    '''enter payment information'''
    
    user = request.user
    rental_request = hmod.Rental_Request.objects.get(id=rental_request_id)
    listing = hmod.Listing.objects.get(id=rental_request.listing.id)
    
    # need to get the listing_date to see whether to use weekend pricing or not
    listing_date = hmod.Listing_Date.objects.get(id=rental_request.listing_date.id)
    # weekday gets the day of the week, with 0 being Monday and 6 being Sunday
    weekday = listing_date.date.weekday()
    if weekday > 4:
        fee_base = listing.price_per_hour_weekend
    else:
        fee_base = listing.price_per_hour

    # then we need to subtract the end time from the start time to get the hours
    # hours = rental_request.end_time - rental_request.start_time
    
    # multiply the hours by the rate and set that equal to the fee variable below?
     
    # Process payment (via Stripe)
    
    # set the price of the venue
    # fee = settings.SUBSCRIPTION_PRICE
    
    # try:
    #     stripe_customer = sub.charge(request, email, fee)
    # except stripe.StripeError as e:
    #     form._errors[NON_FIELD_ERRORS] = form.error_class([e.args[0]])
    #     return render(request, template,
    #         {'form':form,
    #          'STRIPE_PUBLISHABLE_KEY':settings.STRIPE_PUBLISHABLE_KEY}
    #     )              
                
    context = {
    }
    return render(request, 'payment/cc_info.html', context)