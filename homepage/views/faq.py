from django.http import HttpResponse
from django.shortcuts import render

def faq(request):
    output = "This is the faq page."
        
    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/faq.html', context)