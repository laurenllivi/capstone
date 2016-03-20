from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import datetime
from django.core.mail import send_mail
from time import time
import decimal
import stripe
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os

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
            
            # mark the rental request as paid
            # STILL NEED TO ACCOUNT FOR DEPOSITS
            rental_request.full_amount_paid = True
            rental_request.save()
            
            # send a confirmation email
            subject, from_email, to = 'Thank you for your reservation', settings.EMAIL_HOST_USER, user.email

            html_content = render_to_string('payment/reservation_confirmation.html', {'user':user,\
                    'venue_pic': venue_pic, 'listing': listing, 'rental_request': rental_request,\
                     'listing_date': listing_date, 'fee_in_dollars': fee_in_dollars})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.mixed_subtype = 'related'
            msg.attach_alternative(html_content, "text/html")
            
            # fp = open('/static/images/venue-images/' + str(listing.id) + "/" + str(venue_pic.image_name), 'rb')
            # msgImage = MIMEImage(fp.read())
            # fp.close()
            # msgImage.add_header('Content-ID', '<image1>')
            # msg.attach(msgImage)
                 
            msg.send()
            
            # redirect to the success page
            return HttpResponseRedirect('/payment/success/%s/' % rental_request.id)
            
        except stripe.StripeError as se:
            error = se.args[0]
            context.update({'error': error})           
        
    return render(request, 'payment/cc_info.html', context)