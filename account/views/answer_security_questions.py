from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django import forms
from homepage import models as hmod
from django.utils import timezone
from capstone import settings as settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def answer_security_questions(request):
    '''Answer the account security questions in order to reset username'''
    
    # grab the random string from the url params - identifies the user
    recover_username_key = request.GET.get('string')
    rand_string_object = hmod.Recovery_String.objects.get(rand_string=recover_username_key)
    user = hmod.User.objects.get(id=rand_string_object.user.id)
    key_expiration = rand_string_object.expiration
    
    todays_date = timezone.now()
    
    form = Answer_Question_Form(user=user)
    form.fields["security_question"].queryset = hmod.User_Security_Question.objects.filter(user=user)
    
    if request.method == 'POST': 
        form = Answer_Question_Form(request.POST, user=user)
        form.fields["security_question"].queryset = hmod.User_Security_Question.objects.filter(user=user)
        
        if form.is_valid():
            if key_expiration <= todays_date:
                print(str(key_exp))
                raise forms.ValidationError("Your key has expired.")
            else:
                # send the user an email containing the password
                url = "localhost:8000/account/login"
                
                email = user.email
            
                # send an email with reset link
                subject, from_email, to = 'Your Backyardly Username', settings.EMAIL_HOST_USER, email

                html_content = render_to_string('account/recoverUsernameTemplate.html', {'user':user, 'url': url})
                text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.mixed_subtype = 'related'
                msg.attach_alternative(html_content, "text/html")
                 
                msg.send()
            
            return HttpResponseRedirect("/account/username_email_confirmation?type=%s" %('answered'))                   
                
    context = {
        'form': form, 
    }
    return render(request, 'account/answer_security_questions.html', context)
    
class Answer_Question_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(Answer_Question_Form, self).__init__(*args, **kwargs)
    
    
    security_question = forms.ModelChoiceField(queryset=hmod.User_Security_Question.objects.none(), initial=0)
    security_answer = forms.CharField(required=True, widget=forms.TextInput())
        
    def clean(self):
        # make sure the security question is answered correctly
        question = hmod.Security_Question.objects.get(question=self.cleaned_data['security_question'])
        correct_answer = hmod.User_Security_Question.objects.get(user=self.user,security_question=question).answer
        answer = self.cleaned_data['security_answer']
        
        if str(answer).lower() == str(correct_answer).lower():
            pass
        else:
            raise forms.ValidationError('Your answer does not match our records. Try again or pick a different question.')
        