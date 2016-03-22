from django_messages.models import inbox_count_for
from django_messages import models as dmod


def inbox(request):
    if request.user.is_authenticated():
        return {'messages_inbox_count': inbox_count_for(request.user)}
    else:
        return {}


def notifications_processor(request):
    if request.user.is_authenticated():
        new_message_count = dmod.Message.objects.filter(recipient_id=request.user.id).exclude(read=True).count()
        return {'new_message_count': new_message_count}
    else:
        return {}