from django.http import HttpResponse
from django.shortcuts import render

def terms(request):
    output = "This is the terms, conditions, and policies page."
    
    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    return render(request, 'homepage/terms.html', context)


