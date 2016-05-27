from django.http import HttpResponse
from django.shortcuts import render
from homepage import models as hmod

def faq(request):
    FAQs = hmod.FAQ.objects.all()

    context = {
        'faqs': FAQs,
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/faq.html', context)