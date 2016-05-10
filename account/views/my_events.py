from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms
import datetime as dt
from datetime import timedelta

@login_required
def my_events(request):
    
    user = request.user
    event_requests = hmod.Rental_Request.objects.filter(user=user)
    policies = get_cancellation_policies(request)
    
    approved_events = format_event_requests(request, event_requests, user, True, False)
    pending_approval_events = format_event_requests(request, event_requests, user, False, False)
    canceled_requests = format_event_requests(request, event_requests, user, True, True)
        
    context = {
        'user': user,
        'approvedhtml': approved_events.content,
        'pendinghtml': pending_approval_events.content,
        'canceledhtml': canceled_requests.content,
        'policieshtml': policies.content,
    }
    return render_to_response('account/my_events.html', context, RequestContext(request))
    
def format_event_requests(request, event_requests, user, approved, canceled):

    venue_pics_dict = {}
    cancellation_dict = {}
    fees_dict = {}
    days_to_event_dict = {}
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
            
        # add the rental fees to the dictionary for the template
        weekday = event_request.listing_date.date.weekday()
        if weekday > 4:
            fee_base = event_request.listing.price_per_hour_weekend
            weekend = True
        else:
            fee_base = event_request.listing.price_per_hour
            weekend = False    
        hours = event_request.duration()
        rental_fee = hours * fee_base
        # add the rental request ids and rental fees to the dictionary
        fees_dict[event_request.id] = rental_fee


    date_threshold = dt.datetime.now() + timedelta(days=1)

    if approved and not canceled:
        events = hmod.Rental_Request.objects\
            .filter(user=user)\
            .filter(approved=True)\
            .exclude(canceled=True)\
            .filter(listing_date__date__gt=date_threshold)
    elif canceled:
        events = hmod.Rental_Request.objects\
            .filter(user=user).filter(approved=True)\
            .filter(canceled=True)
    else:
        events = hmod.Rental_Request.objects\
            .filter(user=user).exclude(approved=True)\
            .exclude(canceled=True)

    for e in events:
        event_list.append(e)
        cancellation_policy = hmod.Listing_Policy.objects.filter(listing_id=listing.id).first()
        cancellation_policy = hmod.Cancellation_Policy.objects.filter(id=cancellation_policy.cancellation_policy_id).first()
        cancellation_dict[listing.id] = cancellation_policy

        event_date = hmod.Listing_Date.objects.filter(id=e.listing_date_id).first()
        days_to_event = abs((event_date.date - dt.date.today()).days)
        days_to_event_dict[e.id] = days_to_event
        
    context = {
        'user': user,
        'event_list': event_list,
        'venue_pics_dict': venue_pics_dict,
        'approved': approved,
        'canceled': canceled,
        'cancellation_dict': cancellation_dict,
        'days_to_event_dict': days_to_event_dict,
        'fees_dict': fees_dict,
    }

    return render_to_response('account/event_list.html', context, RequestContext(request))
    
def my_events__del_rental_request(request, rental_request_id):
    '''delete a venue request'''


    event_request = hmod.Rental_Request.objects.get(id=rental_request_id)
    # refund_amount = 0
    # if event_request.deposit_paid == True:
    #     # TODO: issue refund if event has been paid for
    event_request.canceled = True
    event_request.canceled_by = "Guest"
    event_request.save()
    
    return HttpResponseRedirect('/account/my_events/')

def get_cancellation_policies(request):
    cancellation_policies = hmod.Cancellation_Policy.objects.all()

    context = {
        'policies': cancellation_policies
    }

    return render_to_response('partials/_cancellation_policy.html', context, RequestContext(request))