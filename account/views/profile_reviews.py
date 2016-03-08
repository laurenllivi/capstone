from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage import models as hmod
from django import forms

@login_required
def profile_reviews(request):
    
    user = request.user
    
    # get the two lists of reviews to display on the page
    reviews_i_wrote = hmod.Review.objects.filter(user=user)
    my_venue_reviews = hmod.Review.objects.filter(listing__in=hmod.Listing.objects.filter(user=user))
        
    context = {
        'user': user,
        'reviews_i_wrote': reviews_i_wrote,
        'my_venue_reviews': my_venue_reviews,
        'range': range(10),  # 5 stars broken into 2 pieces each

    }
    return render(request, 'account/profile_reviews.html', context)

