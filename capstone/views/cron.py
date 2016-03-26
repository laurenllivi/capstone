from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from homepage import models as hmod
import datetime as dt
from capstone import settings

def my_scheduled_job():
    today = dt.date.today()
    days_to_event = 7
    one_week = dt.timedelta(days=days_to_event)
    week_from_today = today + one_week
    dates = hmod.Listing_Date.objects.filter(date=week_from_today)
    date_list = []
    for d in dates:
        date_list.append(d.id)

    reservations = hmod.Rental_Request.objects.filter(approved=True,
                                                      full_amount_paid=False,
                                                      listing_date_id__in=date_list)
    for r in reservations:
        email = r.user.email

        subject, from_email, to = 'Reminder Email', settings.EMAIL_HOST_USER, email

        html_content = render_to_string('capstone/payment_reminder_template.html', {'reservation': r, 'days_to_event': days_to_event})
        text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.mixed_subtype = 'related'
        msg.attach_alternative(html_content, "text/html")

        msg.send()


if __name__ == '__main__':
    my_scheduled_job()