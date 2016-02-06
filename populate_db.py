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
import datetime

######### Add some test data to the system ############################

# Profile pics
ph = hmod.User_Photo()
ph.alt_title = "profile-lauren"
ph.name = "/static/images/lauren.jpg"
ph.save()

ph2 = hmod.User_Photo()
ph2.alt_title = "profile-shelly"
ph2.name = "/static/images/shelly.jpg"
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
l.price_per_hour = 50
l.listing_type = "Backyard"
l.description = "This is a nice, quiet backyard in the countryside. We love having parties and are excited to offer our backyard for the use of your event."
l.sq_footage = 2000
l.num_guests = 200
l.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
l.street = "1030 E State Street"
l.street2 = "Apt. 2A"
l.city = "Lindon"
l.state = "UT"
l.zipcode = "84042"
l.user = u
l.save()

l2 = hmod.Listing()
l2.title = "Beautiful, green backyard with fountains and pool"
l2.category = "Backyard"
l2.price_per_hour = 150
l2.listing_type = "Backyard"
l2.description = "This is a nice, quiet backyard in the countryside. Pool and fountains offer nice scenery. Beautiful lawn."
l2.sq_footage = 4000
l2.num_guests = 400
l2.parking_desc = "There is parking for about 100, and more parking on the street. Might require a short walk if guests have to park a little bit further down the road."
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
l3.street = "1030 E State Street"
l3.street2 = "Apt. 2A"
l3.city = "Lindon"
l3.state = "UT"
l3.zipcode = "84042"
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
l4.street = "1030 E State Street"
l4.street2 = "Apt. 2A"
l4.city = "Lindon"
l4.state = "UT"
l4.zipcode = "84042"
l4.user = u2
l4.save()

# Listing Photo
p = hmod.Listing_Photo()
p.alt_title = "backyard photo"
p.name = "img"
p.listing = l2
p.save()

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
f.name = "Pool"
f.description = "Outdoor pool"
f.save()

# Listing_Feature (association class)
lf = hmod.Listing_Feature()
lf.listing = l
lf.feature = f
lf.save()

## add more here......

# Add_On
ao = hmod.Add_On()
ao.item_name = "Tablecloths"
ao.description = "50 white lace tablecloths"
ao.quantity_available = 50
ao.price_per = 10
ao.listing = l2
ao.save()

# Listing_Date
ld = hmod.Listing_Date()
ld.start_date = datetime.datetime.today()
ld.end_date = datetime.datetime.today()
ld.status = True
ld.listing = l2
ld.save()

# Rental_Request
rr = hmod.Rental_Request()
rr.listing_date = ld
rr.notes = "Is this still available for this day?"
rr.approved = False
rr.user = u
rr.save()

# Transaction
t = hmod.Transaction()
t.date = datetime.datetime.today()
t.price = 150
t.paid = True
t.notes = "Paid through Paypal"
t.renter = u
t.owner = u2
t.listing = l2
t.rental_request = rr
t.save()

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


