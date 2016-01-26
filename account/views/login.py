from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    output = "This is the login page."

    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    return render(request, 'account/login.html', context)
