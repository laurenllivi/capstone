from django.http import HttpResponse
from django.shortcuts import render

def about(request):
    output = "This is the about us page."
    
    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    return render(request, 'homepage/about.html', context)


