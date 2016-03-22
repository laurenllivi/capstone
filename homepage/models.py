from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings
import datetime
import decimal
import stripe

class User_Photo(models.Model):
    '''profile pics for users'''
    image_name = models.CharField(max_length=100, blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True, null=True)
    image_file = models.ImageField(default='profile-images/no-img.jpg')
    
    def __str__(self):
        return self.image_name   

class User(AbstractUser):
    '''Extension of Django's user class'''
    # inherited from AbstractUser:
    # is_active (use a checkbox)
    # is_superuser
    # is_staff (use a checkbox)
    # first_name
    # last_name
    # username
    # email
    # password included
    # date_joined
    # last_login
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ForeignKey('User_Photo', blank=True, null=True)
    stripe_id = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
        
    def charge(self, request, email, fee):
        # Set your secret key: remember to change this to your live secret key
        # in production. See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a Customer
        stripe_customer = stripe.Customer.create(
            card=token,
            description=email
        )

        # Save the Stripe ID to the customer's profile
        self.stripe_id = stripe_customer.id
        self.save()

        # Charge the Customer instead of the card
        stripe.Charge.create(
            amount=fee, # in cents
            currency="usd",
            customer=stripe_customer.id
        )

        return stripe_customer

class Feature(models.Model):
    '''A feature that a listing has'''
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class Cancellation_Policy(models.Model):
    name = models.CharField(max_length=50)
    days_to_cancel = models.IntegerField()
    percent_refunded = models.IntegerField()
    deposit_refunded = models.NullBooleanField(default=False)

    def __str__(self):
        return self.name

class Listing(models.Model):
    '''A venue listing posted by a user'''
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    price_per_hour = models.DecimalField(decimal_places=0, max_digits=8, blank=True, null=True)
    price_per_hour_weekend = models.DecimalField(decimal_places=0, max_digits=8, blank=True, null=True)
    deposit = models.DecimalField(decimal_places=0, max_digits=8, blank=True, null=True)
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    sq_footage = models.IntegerField(blank=True, null=True)
    num_guests = models.IntegerField(blank=True, null=True)
    parking_desc = models.CharField(max_length=1000, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    geolocation = models.PointField(blank=True, null=True)
    currently_listed = models.NullBooleanField(default=False, blank=True)
    is_active = models.NullBooleanField(default=True, blank=True)
    user = models.ForeignKey('User')
    
    def __str__(self):
        return self.title


class Listing_Photo(models.Model):
    '''Photos for listings '''
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_title = models.CharField(max_length=255, blank=True, null=True)
    image_file = models.ImageField(default='venue-images/None/no-img.jpg')
    listing = models.ForeignKey('Listing')
    
    def __str__(self):
        return self.image_name


class Review(models.Model):
    '''A user gives a listing a review'''
    rating = models.DecimalField(decimal_places=1, max_digits=2, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    review_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)


class Listing_Feature(models.Model):
    '''Association class between listing and feature'''
    listing = models.ForeignKey('Listing')
    feature = models.ForeignKey('Feature')


class Add_On(models.Model):
    item_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    quantity_available = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    price_per = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    
class Listing_Date(models.Model):
    '''The dates that the venue is avaible or not . . . false = blocked out, true = available???'''
    # start_date = models.DateTimeField(blank=True, null=True)
    # end_date = models.DateTimeField(blank=True, null=True)
    # status = models.NullBooleanField(default=False, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    listing = models.ForeignKey('Listing')

class Listing_Policy(models.Model):
    cancellation_policy = models.ForeignKey('Cancellation_Policy')
    listing = models.ForeignKey('Listing')
    
class Rental_Request(models.Model):
    '''When a user makes a request to rent a venue'''
    notes = models.CharField(max_length=255, blank=True, null=True)
    approved = models.NullBooleanField(blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(default='19:00')
    end_time = models.TimeField(default='19:00')
    user = models.ForeignKey(User)
    canceled = models.NullBooleanField(default=False, blank=True, null=True)
    canceled_by = models.CharField(max_length=20, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    listing_date = models.ForeignKey('Listing_Date', blank=True, null=True)
    full_amount_paid = models.NullBooleanField(blank=True, null=True, default=False)
    deposit_paid = models.NullBooleanField(blank=True, null=True, default=False)
    viewed_by_owner = models.NullBooleanField(default=False, blank=True, null=True)
    
    def duration(self):
        '''gets the difference between the start and end times (in hours - decimal) - have to combine the times with 
        a dummy date because you can't subtract two Python time objects'''
        dummydate = datetime.date(2000,1,1)
        duration = datetime.datetime.combine(dummydate,self.end_time) - datetime.datetime.combine(dummydate,self.start_time)
        total_seconds = duration.total_seconds()
        hours = total_seconds / 60 / 60
        hours = decimal.Decimal(hours)
        return hours
            
class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    paid = models.NullBooleanField(default=False, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    renter = models.ForeignKey(User, related_name='transaction_renter')
    owner = models.ForeignKey(User, related_name='transaction_owner')
    listing = models.ForeignKey('Listing')
    rental_request = models.ForeignKey('Rental_Request')
    
class Message(models.Model):
    '''A message between two users in the system'''
    time_stamp = models.DateTimeField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)
    read = models.NullBooleanField(default=False, blank=True)
    sender = models.ForeignKey(User, related_name='message_sender')
    recipient = models.ForeignKey(User, related_name='message_recipient')
    
class Recovery_String(models.Model):
    '''Used when a user forgets his or her password'''
    rand_string = models.CharField(max_length=255, blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)

class Image(models.Model):
    image_name = models.CharField(max_length=50, blank=True, null=True)
    image_title = models.CharField(max_length=20, blank=True, null=True)
    image_file = models.ImageField(default='venue-images/None/no-img.jpg')
    listing = models.ForeignKey('Listing')

class Customer_Inquiry(models.Model):
    subject = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User')