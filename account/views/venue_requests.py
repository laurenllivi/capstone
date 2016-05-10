from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import datetime
from datetime import timedelta
from homepage import models as hmod
from capstone import settings
from django import forms
import re

@login_required
def venue_requests(request):

    user = request.user
    listings = hmod.Listing.objects.filter(user_id=user.id)

    new_requests = format_ven_requests(request, listings, user, False, False, False)
    approved_requests = format_ven_requests(request, listings, user, True, False, False)
    cancelled_requests = format_ven_requests(request, listings, user, True, True, False)
    past_events = format_ven_requests(request, listings, user, True, False, True)

    context = {
        'pendinghtml': new_requests.content,
        'approvedhtml': approved_requests.content,
        'canceledhtml': cancelled_requests.content,
        'pasteventshtml': past_events.content,
    }

    return render_to_response('account/venue_requests.html', context, RequestContext(request))

def format_ven_requests(request, listings, user, approved, canceled, past):

    if request.method == 'POST':

        request_string = str(request.POST)
        if 'approveRequest' in request_string:
            ven_request_id = re.search('approveRequest(\d+)', request_string).group(1)
            ven_request = hmod.Rental_Request.objects.get(id=ven_request_id)
            ven_request.approved = True
            ven_request.save()

            if ven_request.approval_email_sent_at is None:
                email = ven_request.user.email

                subject, from_email, to = 'Request Approved', settings.EMAIL_HOST_USER, email

                html_content = render_to_string('account/request_approved_template.html',
                                                {'ven_request': ven_request})
                text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.mixed_subtype = 'related'
                msg.attach_alternative(html_content, "text/html")

                msg.send()
                ven_request.approval_email_sent_at = datetime.datetime.now()
                ven_request.save()

        elif 'denyRequest' in request_string:
            ven_request_id = re.search('denyRequest(\d+)', request_string).group(1)
            ven_request = hmod.Rental_Request.objects.get(id=ven_request_id)
            ven_request.approved = False
            ven_request.save()

        elif 'messageUser' in request_string:
            user_id = re.search('messageUser(\d+)', request_string).group(1)
            print(user_id)

        elif 'cancelRequest' in request_string:
            ven_request_id = re.search('cancelRequest(\d+)', request_string).group(1)
            ven_request = hmod.Rental_Request.objects.get(id=ven_request_id)
            ven_request.canceled = True
            ven_request.canceled_by = "Owner"
            ven_request.save()

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

        date_threshold = datetime.datetime.now() - timedelta(days=1)
        if approved and not canceled and not past:
            # approved future events
            requests = hmod.Rental_Request.objects\
                .filter(listing_id=listing.id)\
                .filter(approved=True)\
                .exclude(canceled=True)\
                .filter(listing_date__date__gt=date_threshold)
        elif canceled:
            # canceled requests
            requests = hmod.Rental_Request.objects\
                .filter(listing_id=listing.id)\
                .filter(canceled=True)
        elif past:
            # events that have happened
            date_threshold = datetime.datetime.now() - timedelta(days=1)
            requests = hmod.Rental_Request.objects\
                .filter(listing_id=listing.id)\
                .filter(approved=True)\
                .filter(canceled=False)\
                .filter(listing_date__date__lt=date_threshold)
        else:
            # new requests
            requests = hmod.Rental_Request.objects\
                .filter(listing_id=listing.id)\
                .exclude(approved=True)\
                .exclude(approved=False)\
                .exclude(canceled=True)\
                .filter(listing_date__date__gt=date_threshold)
            for listing_request in requests:
                listing_request.viewed_by_owner = True
                listing_request.save()

        for i in requests:
            request_list.append(i)


    context = {
        'user': user,
        'request_list': request_list,
        'venue_pics_dict': venue_pics_dict,
        'approved': approved,
        'canceled': canceled,
        'past': past,
    }

    return render_to_response('account/request_list.html', context, RequestContext(request))