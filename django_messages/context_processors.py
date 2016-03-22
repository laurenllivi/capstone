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
        new_request_count = 0
        for listing in user_listings:
            request_count = hmod.Rental_Request.objects.filter(listing_id=listing.id).exclude(viewed_by_owner=True).count()
            new_request_count += request_count

        return {
            'new_message_count': new_message_count,
            'new_request_count': new_request_count
        }
    else:
        return {}