from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime,date,timedelta
from sdcms.manager.models import *

# Create your views here.

def index(request):
    try:
        page = Page.objects.get(slug='index')
    except Page.DoesNotExist:
        page = None

    navitems = Navigation.objects.all()
    return render_to_response('index.html', { 'navitems': navitems,
                                              'page': page, })

def go(request,tag=None):
    try:
        page = Page.objects.get(slug=)
    except Page.DoesNotExist:
        page = None

    navitems = Navigation.objects.all()
    return render_to_response('page.html', { 'navitems': navitems,
                                              'page': page, })
