from django.http import HttpResponse
from django.shortcuts import render

def post_venue(request):
    output = "This is the post venue page."

    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    return render(request, 'venue/post_venue.html', context)