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
from datetime import timedelta
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
l.deposit = 50
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

ld = hmod.Listing_Date()
ld.date = datetime.datetime.now() + timedelta(days=5)
ld.listing = l
ld.save()

ld2 = hmod.Listing_Date()
ld2.date = datetime.datetime.now() + timedelta(days=1)
ld2.listing = l
ld2.save()

rr = hmod.Rental_Request()
rr.approved = False
rr.request_date = datetime.datetime.now()
rr.start_time = '17:00:00'
rr.end_time = '19:00:00'
rr.user = u2
rr.listing = l
rr.listing_date = ld
rr.viewed_by_owner = False
rr.full_amount_paid = False
rr.save()

rr3 = hmod.Rental_Request()
rr3.request_date = datetime.datetime.now()
rr3.approved = True
rr3.start_time = '13:00:00'
rr3.end_time = '15:00:00'
rr3.user = u2
rr3.listing = l
rr3.listing_date = ld2
rr3.full_amount_paid = False
rr3.viewed_by_owner = True
rr3.save()

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
l2.deposit = 50
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

ld3 = hmod.Listing_Date()
ld3.date = datetime.datetime.now()
ld3.listing = l2
ld3.save()

ld4 = hmod.Listing_Date()
ld4.date = datetime.datetime.now() + timedelta(days=2)
ld4.listing = l2
ld4.save()

rr2 = hmod.Rental_Request()
rr2.viewed_by_owner =True
rr2.approved = True
rr2.start_time = '18:00:00'
rr2.end_time = '20:00:00'
rr2.user = u
rr2.listing = l2
rr2.listing_date = ld3
rr2.full_amount_paid = True
rr2.save()

rr4 = hmod.Rental_Request()
rr4.approved = False
rr4.viewed_by_owner = True
rr4.start_time = '18:00:00'
rr4.end_time = '20:00:00'
rr4.user = u2
rr4.listing = l2
rr4.listing_date = ld4
rr4.full_amount_paid = False
rr4.save()

l3 = hmod.Listing()
l3.title = "Large home pool"
l3.category = "Pool"
l3.price_per_hour = 50
l3.price_per_hour_weekend = 150
l3.deposit = 50
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
l4.price_per_hour_weekend = 150
l4.deposit = 50
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

l5 = hmod.Listing()
l5.title = "Gorgeous Backyard"
l5.category = "Backyard"
l5.price_per_hour = 200
l5.price_per_hour_weekend = 250
l5.deposit = 50
l5.listing_type = "Backyard"
l5.description = "Beautiful Backyard"
l5.sq_footage = 2000
l5.num_guests = 200
l5.parking_desc = "Plenty of Parking"
l5.street = "2445 Timpview Drive"
l5.street2 = ""
l5.city = "Provo"
l5.state = "UT"
l5.zipcode = "84604"
g5 = geocoder.google(
    l5.street + " " +
    l5.street2 + " " +
    l5.city + " " +
    l5.state
)
l5.geolocation = Point(float(g5.lat), float(g5.lng))
l5.currently_listed = True
l5.user = u2
l5.save()

l6 = hmod.Listing()
l6.title = "Magical Backyard"
l6.category = "Backyard"
l6.price_per_hour = 200
l6.price_per_hour_weekend = 250
l6.deposit = 50
l6.listing_type = "Backyard"
l6.description = "Beautiful Backyard"
l6.sq_footage = 2000
l6.num_guests = 200
l6.parking_desc = "Plenty of Parking"
l6.street = "1392 N 380 W"
l6.street2 = ""
l6.city = "Provo"
l6.state = "UT"
l6.zipcode = "84604"
g6 = geocoder.google(
    l6.street + " " +
    l6.street2 + " " +
    l6.city + " " +
    l6.state
)
l6.geolocation = Point(float(g6.lat), float(g6.lng))
l6.currently_listed = True
l6.user = u2
l6.save()

l7 = hmod.Listing()
l7.title = "Perfect Yard for Receptions"
l7.category = "Backyard"
l7.price_per_hour = 200
l7.price_per_hour_weekend = 250
l7.deposit = 50
l7.listing_type = "Backyard"
l7.description = "Beautiful Backyard"
l7.sq_footage = 2000
l7.num_guests = 200
l7.parking_desc = "Plenty of Parking"
l7.street = "2445 Timpview Drive"
l7.street2 = ""
l7.city = "Provo"
l7.state = "UT"
l7.zipcode = "84604"
g7 = geocoder.google(
    l7.street + " " +
    l7.street2 + " " +
    l7.city + " " +
    l7.state
)
l7.geolocation = Point(float(g7.lat), float(g7.lng))
l7.currently_listed = True
l7.user = u2
l7.save()

l8 = hmod.Listing()
l8.title = "Beautiful Yard"
l8.category = "Backyard"
l8.price_per_hour = 200
l8.price_per_hour_weekend = 250
l8.deposit = 50
l8.listing_type = "Backyard"
l8.description = "Beautiful Backyard"
l8.sq_footage = 2000
l8.num_guests = 200
l8.parking_desc = "Plenty of Parking"
l8.street = "3322 N Cottonwood Ln"
l8.street2 = ""
l8.city = "Provo"
l8.state = "UT"
l8.zipcode = "84604"
g8 = geocoder.google(
    l8.street + " " +
    l8.street2 + " " +
    l8.city + " " +
    l8.state
)
l8.geolocation = Point(float(g8.lat), float(g8.lng))
l8.currently_listed = True
l8.user = u2
l8.save()

l9 = hmod.Listing()
l9.title = "Well-kept yard"
l9.category = "Backyard"
l9.price_per_hour = 200
l9.price_per_hour_weekend = 250
l9.deposit = 50
l9.listing_type = "Backyard"
l9.description = "Beautiful Backyard"
l9.sq_footage = 2000
l9.num_guests = 200
l9.parking_desc = "Plenty of Parking"
l9.street = "3131 N Cottonwood Ln"
l9.street2 = ""
l9.city = "Provo"
l9.state = "UT"
l9.zipcode = "84604"
g9 = geocoder.google(
    l9.street + " " +
    l9.street2 + " " +
    l9.city + " " +
    l9.state
)
l9.geolocation = Point(float(g9.lat), float(g9.lng))
l9.currently_listed = True
l9.user = u2
l9.save()

l10 = hmod.Listing()
l10.title = "Cool Yard"
l10.category = "Backyard"
l10.price_per_hour = 200
l10.price_per_hour_weekend = 250
l10.deposit = 50
l10.listing_type = "Backyard"
l10.description = "Beautiful Backyard"
l10.sq_footage = 2000
l10.num_guests = 200
l10.parking_desc = "Plenty of Parking"
l10.street = "3511 N Cottonwood Ln"
l10.street2 = ""
l10.city = "Provo"
l10.state = "UT"
l10.zipcode = "84604"
g10 = geocoder.google(
    l10.street + " " +
    l10.street2 + " " +
    l10.city + " " +
    l10.state
)
l10.geolocation = Point(float(g10.lat), float(g10.lng))
l10.currently_listed = True
l10.user = u2
l10.save()

l11 = hmod.Listing()
l11.title = "Luxurioius Yard"
l11.category = "Backyard"
l11.price_per_hour = 200
l11.price_per_hour_weekend = 250
l11.deposit = 50
l11.listing_type = "Backyard"
l11.description = "Beautiful Backyard"
l11.sq_footage = 2000
l11.num_guests = 200
l11.parking_desc = "Plenty of Parking"
l11.street = "3302 N 140 W"
l11.street2 = ""
l11.city = "Provo"
l11.state = "UT"
l11.zipcode = "84604"
g11 = geocoder.google(
    l11.street + " " +
    l11.street2 + " " +
    l11.city + " " +
    l11.state
)
l11.geolocation = Point(float(g11.lat), float(g11.lng))
l11.currently_listed = True
l11.user = u2
l11.save()

l12 = hmod.Listing()
l12.title = "Fantastic Yard"
l12.category = "Backyard"
l12.price_per_hour = 200
l12.price_per_hour_weekend = 250
l12.deposit = 50
l12.listing_type = "Backyard"
l12.description = "Beautiful Backyard"
l12.sq_footage = 2000
l12.num_guests = 200
l12.parking_desc = "Plenty of Parking"
l12.street = "2733 Foothill Dr"
l12.street2 = ""
l12.city = "Provo"
l12.state = "UT"
l12.zipcode = "84604"
g12 = geocoder.google(
    l12.street + " " +
    l12.street2 + " " +
    l12.city + " " +
    l12.state
)
l12.geolocation = Point(float(g12.lat), float(g12.lng))
l12.currently_listed = True
l12.user = u2
l12.save()

l13 = hmod.Listing()
l13.title = "Coolest Yard Ever"
l13.category = "Backyard"
l13.price_per_hour = 200
l13.price_per_hour_weekend = 250
l13.deposit = 50
l13.listing_type = "Backyard"
l13.description = "Beautiful Backyard"
l13.sq_footage = 2000
l13.num_guests = 200
l13.parking_desc = "Plenty of Parking"
l13.street = "2940 Foothill Dr"
l13.street2 = ""
l13.city = "Provo"
l13.state = "UT"
l13.zipcode = "84604"
g13 = geocoder.google(
    l13.street + " " +
    l13.street2 + " " +
    l13.city + " " +
    l13.state
)
l13.geolocation = Point(float(g13.lat), float(g13.lng))
l13.currently_listed = True
l13.user = u2
l13.save()

l14 = hmod.Listing()
l14.title = "Stomp the Yard"
l14.category = "Backyard"
l14.price_per_hour = 200
l14.price_per_hour_weekend = 250
l14.deposit = 50
l14.listing_type = "Backyard"
l14.description = "Beautiful Backyard"
l14.sq_footage = 2000
l14.num_guests = 200
l14.parking_desc = "Plenty of Parking"
l14.street = "3066 N Iroquois Dr"
l14.street2 = ""
l14.city = "Provo"
l14.state = "UT"
l14.zipcode = "84604"
g14 = geocoder.google(
    l14.street + " " +
    l14.street2 + " " +
    l14.city + " " +
    l14.state
)
l14.geolocation = Point(float(g14.lat), float(g14.lng))
l14.currently_listed = True
l14.user = u2
l14.save()

l15 = hmod.Listing()
l15.title = "Wonderful Large Yard"
l15.category = "Backyard"
l15.price_per_hour = 200
l15.price_per_hour_weekend = 250
l15.deposit = 50
l15.listing_type = "Backyard"
l15.description = "Beautiful Backyard"
l15.sq_footage = 2000
l15.num_guests = 200
l15.parking_desc = "Plenty of Parking"
l15.street = "3302 N 140 W"
l15.street2 = ""
l15.city = "Provo"
l15.state = "UT"
l15.zipcode = "84604"
g15 = geocoder.google(
    l15.street + " " +
    l15.street2 + " " +
    l15.city + " " +
    l15.state
)
l15.geolocation = Point(float(g15.lat), float(g15.lng))
l15.currently_listed = True
l15.user = u2
l15.save()


# Listing Photo
p = hmod.Listing_Photo()
p.listing = l
p.image_name = "home-theatre.jpg"
p.image_title = "Home Theatre"
p.image_file = '/static/images/venue-images/1/gazebo.jpg'
p.save()

# Listing Photo
p2 = hmod.Listing_Photo()
p2.listing = l2
p2.image_name = "IMG_0051.JPG"
p2.image_title = "Books"
p2.image_file = '/static/images/venue-images/2/backyard.jpg'
p2.save()

# Listing Photo
p3 = hmod.Listing_Photo()
p3.listing = l2
p3.image_name = "IMG_0178.JPG"
p3.image_title = "Grass"
p3.image_file = '/static/images/venue-images/2/IMG_0178.JPG'
p3.save()

p5 = hmod.Listing_Photo()
p5.listing = l5
p5.image_name = "backyard.jpg"
p5.image_title = "Grass"
p5.image_file = '/static/images/venue-images/5/backyard.jpg'
p5.save()

p6 = hmod.Listing_Photo()
p6.listing = l6
p6.image_name = "backyard.jpg"
p6.image_title = "Grass"
p6.image_file = '/static/images/venue-images/6/backyard.jpg'
p6.save()

p7 = hmod.Listing_Photo()
p7.listing = l7
p7.image_name = "backyard.jpg"
p7.image_title = "Grass"
p7.image_file = '/static/images/venue-images/7/backyard.jpg'
p7.save()

p8 = hmod.Listing_Photo()
p8.listing = l8
p8.image_name = "backyard.jpg"
p8.image_title = "Grass"
p8.image_file = '/static/images/venue-images/8/backyard.jpg'
p8.save()

p9 = hmod.Listing_Photo()
p9.listing = l9
p9.image_name = "backyard.jpg"
p9.image_title = "Grass"
p9.image_file = '/static/images/venue-images/9/backyard.jpg'
p9.save()

p10 = hmod.Listing_Photo()
p10.listing = l10
p10.image_name = "backyard.jpg"
p10.image_title = "Grass"
p10.image_file = '/static/images/venue-images/10/backyard.jpg'
p10.save()

p11 = hmod.Listing_Photo()
p11.listing = l11
p11.image_name = "backyard.jpg"
p11.image_title = "Grass"
p11.image_file = '/static/images/venue-images/11/backyard.jpg'
p11.save()

p12 = hmod.Listing_Photo()
p12.listing = l12
p12.image_name = "backyard.jpg"
p12.image_title = "Grass"
p12.image_file = '/static/images/venue-images/12/backyard.jpg'
p12.save()

p13 = hmod.Listing_Photo()
p13.listing = l13
p13.image_name = "backyard.jpg"
p13.image_title = "Grass"
p13.image_file = '/static/images/venue-images/13/backyard.jpg'
p13.save()

p14 = hmod.Listing_Photo()
p14.listing = l14
p14.image_name = "backyard.jpg"
p14.image_title = "Grass"
p14.image_file = '/static/images/venue-images/14/backyard.jpg'
p14.save()

p15 = hmod.Listing_Photo()
p15.listing = l15
p15.image_name = "backyard.jpg"
p15.image_title = "Grass"
p15.image_file = '/static/images/venue-images/15/backyard.jpg'
p15.save()

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
p.name = 'flexible'
p.days_to_cancel = 2
p.deposit_refunded = True
p.percent_refunded = 100
p.save()

p = hmod.Cancellation_Policy()
p.name = 'moderate'
p.days_to_cancel = 7
p.deposit_refunded = False
p.percent_refunded = 100
p.save()

p = hmod.Cancellation_Policy()
p.name = 'strict'
p.days_to_cancel = 14
p.deposit_refunded = False
p.percent_refunded = 80
p.save()

lp = hmod.Listing_Policy()
lp.listing_id = 1
lp.cancellation_policy_id = 2
lp.save()

lp2 = hmod.Listing_Policy()
lp2.listing_id = 2
lp2.cancellation_policy_id = 2
lp2.save()

lp3 = hmod.Listing_Policy()
lp3.listing_id = 3
lp3.cancellation_policy_id = 2
lp3.save()

lp4 = hmod.Listing_Policy()
lp4.listing_id = 4
lp4.cancellation_policy_id = 2
lp4.save()

lp5 = hmod.Listing_Policy()
lp5.listing_id = 5
lp5.cancellation_policy_id = 2
lp5.save()

lp6 = hmod.Listing_Policy()
lp6.listing_id = 6
lp6.cancellation_policy_id = 2
lp6.save()

lp7 = hmod.Listing_Policy()
lp7.listing_id = 7
lp7.cancellation_policy_id = 2
lp7.save()

lp8 = hmod.Listing_Policy()
lp8.listing_id = 8
lp8.cancellation_policy_id = 2
lp8.save()

lp9 = hmod.Listing_Policy()
lp9.listing_id = 9
lp9.cancellation_policy_id = 2
lp9.save()

lp10 = hmod.Listing_Policy()
lp10.listing_id = 10
lp10.cancellation_policy_id = 2
lp10.save()

lp11 = hmod.Listing_Policy()
lp11.listing_id = 11
lp11.cancellation_policy_id = 2
lp11.save()

lp12 = hmod.Listing_Policy()
lp12.listing_id = 12
lp12.cancellation_policy_id = 2
lp12.save()

lp13 = hmod.Listing_Policy()
lp13.listing_id = 13
lp13.cancellation_policy_id = 2
lp13.save()

lp14 = hmod.Listing_Policy()
lp14.listing_id = 14
lp14.cancellation_policy_id = 2
lp14.save()

lp15 = hmod.Listing_Policy()
lp15.listing_id = 15
lp15.cancellation_policy_id = 2
lp15.save()

## add more here......

# Add_On
ao = hmod.Add_On()
ao.item_name = "Tablecloths"
ao.description = "50 white lace tablecloths"
ao.quantity_available = 50
ao.price_per = 10
ao.listing = l2
ao.save()

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
m.read = True
m.save()

m2 = mmod.Message()
m2.subject = "We had a great time"
m2.body = "We appreciated the hospitality when we rented out your backyard for our reception last weekend. Thank you, and I'll be sure to leave you a nice review! :)"
m2.sender = u
m2.recipient = u2
m2.sent_at = datetime.datetime.now()
m2.read_at = datetime.datetime.now()
m2.read = True
m2.save()

m3 = mmod.Message()
m3.subject = "Thanks for emailing me"
m3.body = "Thanks for the message. I'm excited to rent out your theatre for my family reunion next month!"
m3.sender = u2
m3.recipient = u
m3.sent_at = datetime.datetime.now()
m3.read_at = datetime.datetime.now()
m3.read = True
m3.save()

m4 = mmod.Message()
m4.subject = "We had a great time"
m4.body = "We appreciated the hospitality when we rented out your backyard for our reception last weekend. Thank you, and I'll be sure to leave you a nice review! :)"
m4.sender = u2
m4.recipient = u
m4.sent_at = datetime.datetime.now()
m4.read_at = datetime.datetime.now()
m4.read = True
m4.save()
