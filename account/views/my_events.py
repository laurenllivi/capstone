from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
from django.template.defaulttags import register

@login_required
def my_events(request):
    
    user = request.user
    event_requests = hmod.Rental_Request.objects.filter(user=user)
    
    approved_events = format_event_requests(request, event_requests, user, True, False)
    pending_approval_events = format_event_requests(request, event_requests, user, False, False)
    canceled_requests = format_event_requests(request, event_requests, user, True, True)
        
    context = {
        'user': user,
        'approvedhtml': approved_events.content,
        'pendinghtml': pending_approval_events.content,
        'canceledhtml': canceled_requests.content,
    }
    return render_to_response('account/my_events.html', context, RequestContext(request))
    
def format_event_requests(request, event_requests, user, approved, canceled):

    venue_pics_dict = {}
    event_list = []

    for event_request in event_requests:
        listing = hmod.Listing.objects.get(id=event_request.listing.id)
        try:
            # get only the first pic from the venue
            venue_pic = hmod.Listing_Photo.objects.filter(listing=listing).first()
            # and add it to the dictionary
            venue_pics_dict[listing.id] = venue_pic

        except hmod.Listing_Photo.DoesNotExist:
            pass

        if approved and not canceled:
            events = hmod.Rental_Request.objects.filter(user=user, approved=True).exclude(canceled=True)
        elif canceled:
            events = hmod.Rental_Request.objects.filter(user=user, approved=True, canceled=True)
        else:
            events = hmod.Rental_Request.objects.filter(user=user).exclude(approved=True).exclude(canceled=True)

        for e in events:
            event_list.append(e)

    context = {
        'user': user,
        'event_list': event_list,
        'venue_pics_dict': venue_pics_dict,
        'approved': approved,
        'canceled': canceled,
    }

    return render_to_response('account/event_list.html', context, RequestContext(request))
    
def my_events__del_rental_request(request, rental_request_id):
    '''delete a venue request'''
    
    event_request = hmod.Rental_Request.objects.get(id=rental_request_id)
    event_request.canceled = True
    event_request.canceled_by = "Guest"
    event_request.save()
    
    return HttpResponseRedirect('/account/my_events/')