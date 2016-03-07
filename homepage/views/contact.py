from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.contrib.auth.decorators import login_required
from lib import choices

@login_required
def contact(request):
    user = request.user
    form = ContactForm
    message = ''

    if request.method == 'POST':
        print 'method was post'
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        form = ContactForm(request.POST)

        if form.is_valid():
            message = 'Thanks for the message!'
            inquiry = hmod.Customer_Inquiry()
            inquiry.subject = form.cleaned_data['subject']
            inquiry.message = form.cleaned_data['message']
            inquiry.user = user
            inquiry.save()


    # the equivalent of template_vars in DMP
    context = {
        'form': form,
        'message': message
    }
    # return HttpResponse(template.render(context, request))
    # below is the shortcut to use instead of the line above
    return render(request, 'homepage/contact.html', context)


class ContactForm(forms.Form):
    subject = forms.ChoiceField(widget=forms.Select(), choices=choices.QUESTION_TOPICS)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Your Message', 'rows': 6}))
