from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
    output = "This is a test."
    
    template = loader.get_template('homepage/index.html')
    
    # the equivalent of template_vars in DMP
    context = {
        'output' : output,
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/index.html', context)


