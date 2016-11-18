from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.db.models import Q
from datetime import datetime,date,timedelta
from mgr.models import *
from mgr.forms import *

# Create your views here.

def index(request):
    try:
        page = Page.objects.get(slug='index')
    except Page.DoesNotExist:
        page = None

    navitems = NavigationItem.objects.filter(parent__isnull=True)
    nav2items = NavigationItem.objects.filter(parent_id=4)
    pages = navitems.values('page')
    sections = {}
    for s in Section.objects.filter(page=page):
        sections[s.slug] = { 'heading': s.title, 'content': s.content }
    sidebar = Section.objects.get(slug='sidebar')
    return render(request, 'index.html', {
        'navitems': navitems,
        'nav2items': nav2items,
        'sidebar': sidebar,
        'page': page,
        'sections': sections,
    })


def go(request,page_name=None):
    templ = 'page.html'
    try:
        page = Page.objects.get(slug=page_name)
    except Page.DoesNotExist:
        page = None

    navitems = NavigationItem.objects.all()
#    if page and page.template:
#        templ = 'media/' + page.template.html.name
    sidebar = Section.objects.get(slug='sidebar')
    return render(request, templ, {
        'navitems': navitems,
        'sidebar': sidebar,
        'page': page
    })


def gallery(request,gal_id=None):
    gallery = None
    if gal_id:
        gallery = Gallery.objects.get(pk=gal_id)

    galleries = Gallery.objects.all()
    navitems = NavigationItem.objects.all()

    return render(request, 'gallery.html', {'gallery': gallery,
                                               'galleries': galleries,
                                               'navitems': navitems, })


def news(request,blog_id=None):
    article = None
    articles = Article.objects.filter(published=True) # [:5] # limit 5?
    if blog_id:
        article = Article.objects.get(pk=blog_id)
    if not article:
        article = articles[0]

    articles = articles.exclude(pk=article.pk) # [:5] # limit 5?
    navitems = NavigationItem.objects.all()

    return render(request, 'news.html', {
        'article': article,
        'articles': articles,
        'navitems': navitems
    })


def contact(request):
    TO_EMAIL = 'info@solomonslutheran.org'
    FROM_EMAIL = 'dennis@mercersburg.net'
    SUBJECT = 'Web site submission'
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_mail(SUBJECT, contact.to_msg(),
                      FROM_EMAIL, [TO_EMAIL],fail_silently=False)
            return HttpResponseRedirect(request.POST.get('redirect','/'))
    else:
        form = ContactForm()
    navitems = NavigationItem.objects.all()
    page = Page.objects.get(slug='contact')
    return render(request, 'contact.html', {
        'form': form,
        'page': page,
        'navitems': navitems
    })
