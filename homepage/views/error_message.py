from django.http import HttpResponse
from django.shortcuts import render

def error_message(request):
    
    context = {
        
    }
    return render(request, 'homepage/error_message.html', context)


