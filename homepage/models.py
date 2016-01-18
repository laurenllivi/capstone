from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings

class Address(models.Model):
    '''Address object'''   
    address_type = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.street
        
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
    # password included??
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.ForeignKey('Address')
    
    def __str__(self):
        return self.first_name + " " + self.last_name
        
class Listing(models.Model):
    '''A venue listing posted by a user'''
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    sq_footage = models.IntegerField(blank=True, null=True)
    num_guests = models.IntegerField(blank=True, null=True)
    parking_desc = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('User')
    address = models.ForeignKey('Address')
    
    def __str__(self):
        return self.title
    
class Photo(models.Model):
    '''Photos for either the listing or a user'''
    alt_title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    listing = models.ForeignKey('Listing', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    '''A user gives a listing a review'''
    rating = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    user = models.ForeignKey(User)
    
class Feature(models.Model):
    '''A feature that a listing has'''
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name
        
class Listing_Feature(models.Model):
    '''Association class between listing and feature'''
    listing = models.ForeignKey('Listing')
    feature = models.ForeignKey('Feature')
        
class Add_On(models.Model):
    item_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity_available = models.CharField(max_length=255, blank=True, null=True)
    price_per = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    
class Listing_Date(models.Model):
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.NullBooleanField(default=False, blank=True, null=True)
    listing = models.ForeignKey('Listing')
    
class Rental_Request(models.Model):
    notes = models.CharField(max_length=255, blank=True, null=True)
    approved = models.NullBooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(User)
    listing_date = models.ForeignKey('Listing_Date')
    
class Transaction(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    paid = models.NullBooleanField(default=False, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    renter = models.ForeignKey(User, related_name='transaction_renter')
    owner = models.ForeignKey(User, related_name='transaction_owner')
    listing = models.ForeignKey('Listing')
    rental_request = models.ForeignKey('Rental_Request')
    
class Message(models.Model):
    time_stamp = models.DateTimeField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)
    sender = models.ForeignKey(User, related_name='message_sender')
    recipient = models.ForeignKey(User, related_name='message_recipient')
    
class Recovery_String(models.Model):
    '''Used when a user forgets his or her password'''
    rand_string = models.CharField(max_length=255, blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)




    
    

    
   
        
    
        