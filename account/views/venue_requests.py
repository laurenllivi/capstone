from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
import re

@login_required
def venue_requests(request):

    user = request.user
    listings = hmod.Listing.objects.filter(user_id=user.id)

    new_requests = format_ven_requests(request, listings, user, False, False)
    approved_requests = format_ven_requests(request, listings, user, True, False)
    cancelled_requests = format_ven_requests(request, listings, user, True, True)

    context = {
        'pendinghtml': new_requests.content,
        'approvedhtml': approved_requests.content,
        'canceledhtml': cancelled_requests.content,
    }

    return render_to_response('account/venue_requests.html', context, RequestContext(request))

def format_ven_requests(request, listings, user, approved, canceled):

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

        if approved and not canceled:
            requests = hmod.Rental_Request.objects.filter(listing_id=listing.id).filter(approved=True).exclude(canceled=True)
        elif canceled:
            requests = hmod.Rental_Request.objects.filter(listing_id=listing.id).filter(canceled=True)
        else:
            requests = hmod.Rental_Request.objects\
                .filter(listing_id=listing.id)\
                .exclude(approved=True)\
                .exclude(approved=False)\
                .exclude(canceled=True)
            for listing_request in requests:
                listing_request.viewed_by_owner = True
                listing_request.save()

        for i in requests:
            request_list.append(i)

    if request.method == 'POST':

        request_string = str(request.POST)
        if 'approveRequest' in request_string:
            ven_request_id = re.search('approveRequest(\d+)', request_string).group(1)
            ven_request = hmod.Rental_Request.objects.get(id=ven_request_id)
            ven_request.approved = True
            ven_request.save()

        elif 'denyRequest' in request_string:
            ven_request_id = re.search('denyRequest(\d+)', request_string).group(1)
            ven_request = hmod.Rental_Request.objects.get(id=ven_request_id)
            ven_request.approved = False
            ven_request.save()

        elif 'messageUser' in request_string:
            user_id = re.search('messageUser(\d+)', request_string).group(1)
            print(user_id)


    context = {
        'user': user,
        'request_list': request_list,
        'venue_pics_dict': venue_pics_dict,
        'approved': approved,
        'canceled': canceled,
    }

    return render_to_response('account/request_list.html', context, RequestContext(request))