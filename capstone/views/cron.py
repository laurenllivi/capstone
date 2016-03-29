from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from homepage import models as hmod
import datetime as dt
from capstone import settings

def run_daily():
    #
    # send a reminder email to pay one week before the event
    #
    today = dt.date.today()

    days_to_event = 7
    date_ids = get_date_ids(today, days_to_event)

    # get all reservations that have been approved but not paid that are one week from today
    reservations = get_reservations(date_ids)
    send_reminder_email(reservations, days_to_event)

    #
    # send a reminder email to pay 3 days before the event
    #
    days_to_event = 3
    date_ids = get_date_ids(today, days_to_event)
    reservations_soon = get_reservations(date_ids)

    send_reminder_email(reservations_soon, days_to_event)


    #
    # cancel all unpaid events in two days
    #
    days_to_event = 2
    date_ids = get_date_ids(today, days_to_event)
    reservations_to_cancel = get_reservations(date_ids)
    cancel_reservations(reservations_to_cancel)


def get_date_ids(today, days_from_today):
    days_from_today = dt.timedelta(days=days_from_today)
    target_date = today + days_from_today
    dates = hmod.Listing_Date.objects.filter(date=target_date)
    date_list = []
    for d in dates:
        date_list.append(d.id)

    return date_list


def get_reservations(days_to_event):
    reservations = hmod.Rental_Request.objects.filter(approved=True,
                                                      full_amount_paid=False,
                                                      listing_date_id__in=days_to_event).exclude(canceled=True)
    return reservations


def send_reminder_email(reservations, days_to_event):

    #send an email for each reservation
    for r in reservations:
        email = r.user.email

        subject, from_email, to = 'Reminder Email', settings.EMAIL_HOST_USER, email

        html_content = render_to_string('capstone/payment_reminder_template.html',
                                        {'reservation': r, 'days_to_event': days_to_event})
        text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.mixed_subtype = 'related'
        msg.attach_alternative(html_content, "text/html")

        msg.send()


def cancel_reservations(reservations):
    for r in reservations:
        r.canceled = True
        r.canceled_by = "Unpaid"
        r.save()

if __name__ == '__main__':
    my_scheduled_job()