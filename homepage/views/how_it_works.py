from django.http import HttpResponse
from django.shortcuts import render

def HowItWorks(request):
    output = "This is the how it works page."

    # the equivalent of template_vars in DMP
    context = {
        'output': output,
    }
    return render(request, 'homepage/how-it-works.html', context)