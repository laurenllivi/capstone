from django.http import HttpResponse
from django import forms
import json
from django.shortcuts import *
from django.template import RequestContext

def test(request):

    response = test_form(request)


    context = {
        'formhtml': response.content,
    }
    return render_to_response('venue/test.html', context, RequestContext(request))




def test_form(request):
    form = TestForm()

    if request.method == 'POST':
        form = TestForm(request.POST)
        print form

        message = 'something wrong!'
        if form.is_valid():
            print(request.POST['text'])
            message = request.POST['text']

    context = {
        'form': form,
    }
    return render_to_response('venue/test_form.html', context, RequestContext(request))


class TestForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.TextInput())

