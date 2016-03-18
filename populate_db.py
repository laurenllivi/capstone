#!/usr/bin/python

# use this script after recreating the database

# initialize django
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "capstone.settings"

import django
django.setup()
# imports
from django.conf import settings
from homepage import models as hmod
from django_messages import models as mmod
import datetime
from django.contrib.gis.geos import Point
import geocoder

os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")

######### Add some test data to the system ############################

# Profile pics
ph = hmod.User_Photo()
ph.image_title = "profile-lauren"
ph.image_name = "profile-lauren"
ph.image_file = "/static/images/profile-images/lauren.jpg"
ph.save()

ph2 = hmod.User_Photo()
ph2.image_title = "profile-shelly"
ph2.image_name = "profile-shelly"
ph2.image_file = "/static/images/profile-images/shelly.jpg"
ph2.save()

# User
u = hmod.User()
u.first_name = "Lauren"
u.last_name = "Livingston"
u.username = "laurenll"
u.set_password('1234')
u.email = "laurenl@fiber.net"
u.phone = "8016168231"
u.is_active = True
u.profile_pic = ph
u.save()

u2 = hmod.User()
u2.first_name = "Shelly"
u2.last_name = "Burbidge"
u2.username = "shellyb"
u2.set_password('1234')
u2.email = "shelly.burbidge@gmail.com"
u2.phone = "8016678890"
u2.is_active = True
u2.profile_pic = ph2
u2.save()

# Listing
l = hmod.Listing()
l.title = "Nice, quiet country backyard"
l.category = "Backyard"
l.listing_type = "Backyard"
l.description = "This is a nice, quiet backyard in the countryside. We love having parties and are excited to offer our backyard for the use of your event."
l.sq_footage = 2000
l.num_guests = 200
l.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
l.street = "700 E 500 N"
l.street2 = ""
l.city = "Provo"
l.state = "UT"
l.zipcode = "84606"
l.price_per_hour = 100
l.price_per_hour_weekend = 150
g = geocoder.google(
    l.street + " " +
    l.street2 + " " +
    l.city + " " +
    l.state
)
l.geolocation = Point(float(g.lat), float(g.lng))
l.currently_listed = True
l.user = u
l.save()

l2 = hmod.Listing()
l2.title = "Beautiful, green backyard with fountains and pool"
l2.category = "Backyard"
l2.listing_type = "Backyard"
l2.description = "This is a nice, quiet backyard in the countryside. Pool and fountains offer nice scenery. Beautiful lawn."
l2.sq_footage = 4000
l2.num_guests = 400
l2.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
l2.street = "260 E 500 N"
l2.street2 = ""
l2.city = "Provo"
l2.state = "UT"
l2.zipcode = "84606"
l2.price_per_hour = 100
l2.price_per_hour_weekend = 150
g2 = geocoder.google(
    l2.street + " " +
    l2.street2 + " " +
    l2.city + " " +
    l2.state
)
l2.geolocation = Point(float(g2.lat), float(g2.lng))
l2.currently_listed = True
l2.user = u2
l2.save()

l3 = hmod.Listing()
l3.title = "Large home pool"
l3.category = "Pool"
l3.price_per_hour = 50
l3.listing_type = "Pool"
l3.description = "This is a nice, quiet backyard in the countryside. We love having parties and are excited to offer our backyard for the use of your event."
l3.sq_footage = 2000
l3.num_guests = 200
l3.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
l3.street = "5000 Forbes Avenue"
l3.street2 = ""
l3.city = "Pittsburgh"
l3.state = "PA"
l3.zipcode = "15232"
g3 = geocoder.google(
    l3.street + " " +
    l3.street2 + " " +
    l3.city + " " +
    l3.state
)
l3.geolocation = Point(float(g3.lat), float(g3.lng))
l3.currently_listed = False
l3.user = u
l3.save()

l4 = hmod.Listing()
l4.title = "Large home pool"
l4.category = "Pool"
l4.price_per_hour = 50
l4.listing_type = "Pool"
l4.description = "This is a nice, quiet backyard in the countryside. We love having parties and are excited to offer our backyard for the use of your event."
l4.sq_footage = 2000
l4.num_guests = 200
l4.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
l4.street = "1030 East Center Street"
l4.street2 = ""
l4.city = "Lindon"
l4.state = "UT"
l4.zipcode = "84042"
g4 = geocoder.google(
    l4.street + " " +
    l4.street2 + " " +
    l4.city + " " +
    l4.state
)
l4.geolocation = Point(float(g4.lat), float(g4.lng))
l4.currently_listed = False
l4.user = u2
l4.save()

# Listing Photo
p = hmod.Listing_Photo()
p.listing = l
p.image_name = "home-theatre.jpg"
p.image_title = "Home Theatre"
p.image_file = '/static/images/venue-images/1/home-theatre.jpg'
p.save()

# Listing Photo
p2 = hmod.Listing_Photo()
p2.listing = l2
p2.image_name = "IMG_0051.JPG"
p2.image_title = "Books"
p2.image_file = '/static/images/venue-images/2/IMG_0051.JPG'
p2.save()

# Listing Photo
p3 = hmod.Listing_Photo()
p3.listing = l2
p3.image_name = "IMG_0178.JPG"
p3.image_title = "Grass"
p3.image_file = '/static/images/venue-images/2/IMG_0178.JPG'
p3.save()

# Review
r = hmod.Review()
r.rating = 5
r.description = "Our event was FANTASTIC due to the hospitality and well-kept yard of the Burbidge's. Thank you!"
r.listing = l2
r.user = u2
r.save()

r2 = hmod.Review()
r2.rating = 4
r2.description = "Great experience. Beautiful yard."
r2.listing = l
r2.user = u
r2.save()

# Feature
f = hmod.Feature()
f.name = "Waterfall"
f.description = "Outdoor waterfall"
f.save()

f2 = hmod.Feature()
f2.name = "Pool"
f2.description = "Outdoor pool"
f2.save()

f3 = hmod.Feature()
f3.name = "Garden"
f3.description = "Pretty Garden"
f3.save()

f4 = hmod.Feature()
f4.name = "Gazebo"
f4.description = "Like you're practically in the Sound of Music"
f4.save()

# Listing_Feature (association class)
lf = hmod.Listing_Feature()
lf.listing = l
lf.feature = f
lf.save()


# Cancellation Policy
p = hmod.Cancellation_Policy()
p.title = 'flexible'
p.days_to_cancel = 2
p.deposit_refunded = True
p.percent_refunded = 100
p.save()

p = hmod.Cancellation_Policy()
p.title = 'moderate'
p.days_to_cancel = 7
p.deposit_refunded = False
p.percent_refunded = 100
p.save()

p = hmod.Cancellation_Policy()
p.title = 'strict'
p.days_to_cancel = 14
p.deposit_refunded = False
p.percent_refunded = 80
p.save()


## add more here......

# Add_On
ao = hmod.Add_On()
ao.item_name = "Tablecloths"
ao.description = "50 white lace tablecloths"
ao.quantity_available = 50
ao.price_per = 10
ao.listing = l2
ao.save()

# # Listing_Date
# ld = hmod.Listing_Date()
# #ld.start_date = datetime.datetime.today()
# #ld.end_date = datetime.datetime.today()
# #ld.status = True
# ld.listing = l2
# ld.save()

# # Rental_Request
# rr = hmod.Rental_Request()
# rr.listing_date = ld
# rr.notes = "Is this still available for this day?"
# rr.approved = False
# rr.user = u
# rr.save()

# # Transaction
# t = hmod.Transaction()
# t.date = datetime.datetime.today()
# t.price = 150
# t.paid = True
# t.notes = "Paid through Paypal"
# t.renter = u
# t.owner = u2
# t.listing = l2
# t.rental_request = rr
# t.save()

# Message
m = hmod.Message()
m.time_stamp = datetime.datetime.today()
m.subject = "Is this available?"
m.body = "I was just wondering if this property is still available for the 22nd. I would love to host our daughter's reception in your backyard."
m.sender = u2
m.recipient = u
m.save()

# Recovery String
rs = hmod.Recovery_String()
rs.rand_string = "asdjflasdjfl;asdjflk;asdf"
rs.expiration = datetime.datetime.today()
rs.user = u
rs.save()

# Messages
m = mmod.Message()
m.subject = "Thanks for emailing me"
m.body = "Thanks for the message. I'm excited to rent out your theatre for my family reunion next month!"
m.sender = u
m.recipient = u2
m.sent_at = datetime.datetime.now()
m.read_at = datetime.datetime.now()
m.save()

m2 = mmod.Message()
m2.subject = "We had a great time"
m2.body = "We appreciated the hospitality when we rented out your backyard for our reception last weekend. Thank you, and I'll be sure to leave you a nice review! :)"
m2.sender = u
m2.recipient = u2
m2.sent_at = datetime.datetime.now()
m2.read_at = datetime.datetime.now()
m2.save()

m3 = mmod.Message()
m3.subject = "Thanks for emailing me"
m3.body = "Thanks for the message. I'm excited to rent out your theatre for my family reunion next month!"
m3.sender = u2
m3.recipient = u
m3.sent_at = datetime.datetime.now()
m3.read_at = datetime.datetime.now()
m3.save()

m4 = mmod.Message()
m4.subject = "We had a great time"
m4.body = "We appreciated the hospitality when we rented out your backyard for our reception last weekend. Thank you, and I'll be sure to leave you a nice review! :)"
m4.sender = u2
m4.recipient = u
m4.sent_at = datetime.datetime.now()
m4.read_at = datetime.datetime.now()
m4.save()
