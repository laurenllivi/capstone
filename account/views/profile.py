from django.http import HttpResponse
from django.shortcuts import render

def profile(request):
    output = "This will be the account profile page"

    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    return render(request, 'account/profile.html', context)
