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
    reservations = get_reservations(date_ids, False)
    send_payment_reminder(reservations, days_to_event)

    #
    # send a reminder email to pay 3 days before the event
    #
    days_to_event = 3
    date_ids = get_date_ids(today, days_to_event)
    reservations_soon = get_reservations(date_ids, False)

    send_payment_reminder(reservations_soon, days_to_event)


    #
    # send reminder 3 days before the event (paid)
    #
    reservations = get_reservations(date_ids, True)
    send_event_reminder(reservations, days_to_event)


    #
    # cancel all unpaid events that are one day away
    #
    days_to_event = 1
    date_ids = get_date_ids(today, days_to_event)
    reservations_to_cancel = get_reservations(date_ids, False)
    cancel_reservations(reservations_to_cancel)

    # TODO:: send email telling user the event was canceled

    #
    # send email for invitation to review a venue
    #
    past_date = -2
    past_date_ids = get_date_ids(today, past_date)
    reservations_for_reviews = get_reservations(past_date_ids)
    send_review_email(reservations_for_reviews)


def get_date_ids(today, days_from_today):
    days_from_today = dt.timedelta(days=days_from_today)
    target_date = today + days_from_today
    dates = hmod.Listing_Date.objects.filter(date=target_date)
    date_list = []
    for d in dates:
        date_list.append(d.id)

    return date_list


def get_reservations(days_to_event, has_been_paid):
    reservations = hmod.Rental_Request.objects.filter(approved=True,
                                                      full_amount_paid=has_been_paid,
                                                      listing_date_id__in=days_to_event).exclude(canceled=True)
    return reservations


def send_payment_reminder(reservations, days_to_event):
    #send an email for each reservation
    for r in reservations:
        email = r.user.email

        subject, from_email, to = 'Your event is almost here!', settings.EMAIL_HOST_USER, email

        html_content = render_to_string('capstone/payment_reminder_template.html',
                                        {'reservation': r, 'days_to_event': days_to_event})

        send_email(subject, from_email, to, html_content)


def send_event_reminder(reservations, days_to_event):
    #send an email for each reservation
    for r in reservations:
        email = r.user.email

        subject, from_email, to = 'Your event is almost here!', settings.EMAIL_HOST_USER, email

        html_content = render_to_string('capstone/event_reminder_template.html',
                                        {'reservation': r, 'days_to_event': days_to_event})

        send_email(subject, from_email, to, html_content)

def send_review_email(reservations):

    #send an email asking for a review
    for r in reservations:
        email = r.user.email

        subject, from_email, to = "We'd love to hear your feedback!", settings.EMAIL_HOST_USER, email

        html_content = render_to_string('capstone/review_reminder_template.html',
                                        {'reservation': r})

        send_email(subject, from_email, to, html_content)


def send_email(subject, from_email, to, html_content):
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