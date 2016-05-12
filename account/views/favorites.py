from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from homepage import models as hmod

@login_required
def favorites(request):

    user = request.user

    context = {
        'user': user
    }

    return render_to_response('account/favorites.html', context, RequestContext(request))