from django_messages.models import inbox_count_for
from django_messages import models as dmod
from homepage import models as hmod


def inbox(request):
    if request.user.is_authenticated():
        return {'messages_inbox_count': inbox_count_for(request.user)}
    else:
        return {}


def notifications_processor(request):
    if request.user.is_authenticated():
        
        new_message_count = dmod.Message.objects.filter(recipient_id=request.user.id).exclude(read=True).count()
        user_listings = hmod.Listing.objects.filter(user_id=request.user.id)
        paid_rental_requests = hmod.Rental_Request.objects.filter(user_id=request.user.id)
        
        new_request_count = 0
        confirmed_count = 0
        approved_request_count = 0 
        for listing in user_listings:
            # get a list/count of new rental requests
            new_request_list = hmod.Rental_Request.objects.filter(listing_id=listing.id).exclude(viewed_by_owner=True)
            request_count = new_request_list.count()
            new_request_count += request_count
            
            # STILL WORKING ON THIS PART
            # get a list of confirmed reservations (the deposit has been paid)
            confirmed_reservations = hmod.Rental_Request.objects.filter(listing_id=listing.id).exclude(deposit_paid=False)
            confirmed_count = confirmed_reservations.count()
            
            # get a list of rental requests that have been approved
            approved_requests = hmod.Rental_Request.objects.filter(listing_id=listing.id).exclude(approved=False)
            approved_request_count = approved_requests.count()
                       
        # get a list/count of new payments
        payment_notifications = 0    
        

        return {
            'new_message_count': new_message_count,
            'new_request_count': new_request_count,
            'payment_notifications': payment_notifications,
            'new_request_list': new_request_list,
            'confirmed_reservations': confirmed_reservations,
            'approved_requests': approved_requests,
            'approved_request_count': approved_request_count,
        }
    else:
        return {}