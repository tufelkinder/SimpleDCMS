from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime,date,timedelta
from sdcms.manager.models import *

# Create your views here.

def index(request):
    try:
        page = Page.objects.get(slug='index')
    except Page.DoesNotExist:
        page = None

    navitems = NavigationItem.objects.all()
    return render_to_response('index.html', { 'navitems': navitems,
                                              'page': page, })


def go(request,page_name=None):
    templ = 'page.html'
    try:
        page = Page.objects.get(slug=page_name)
    except Page.DoesNotExist:
        page = None

    navitems = NavigationItem.objects.all()
    if page.template:
        templ = 'media/' + page.template.html
    return render_to_response(templ, {'navitems': navitems,
                                      'page': page, })


def gallery(request,gal_id=None):
    gallery = None
    if gal_id:
        gallery = Gallery.objects.get(pk=gal_id)

    galleries = Gallery.objects.all()

    return render_to_response('gallery.html', {'gallery': gallery,
                                               'galleries': galleries, })


def blog(request,blog_id=None):
    article = None
    if blog_id:
        article = Article.objects.get(pk=blog_id)

    articles = Article.objects.all() # [:5] # limit 5?

    return render_to_response('blog.html', {'article': article,
                                            'articles': articles, })

