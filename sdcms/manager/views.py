from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from datetime import datetime,date,timedelta
from sdcms.manager.models import *
from sdcms.manager.forms import *

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
    if page and page.template:
        templ = 'media/' + page.template.html
    return render_to_response(templ, {'navitems': navitems,
                                      'page': page, })


def gallery(request,gal_id=None):
    gallery = None
    if gal_id:
        gallery = Gallery.objects.get(pk=gal_id)

    galleries = Gallery.objects.all()
    navitems = NavigationItem.objects.all()

    return render_to_response('gallery.html', {'gallery': gallery,
                                               'galleries': galleries,
                                               'navitems': navitems, })


def blog(request,blog_id=None):
    article = None
    articles = Article.objects.filter(published=True) # [:5] # limit 5?
    if blog_id:
        article = Article.objects.get(pk=blog_id)
    if not article:
        article = articles[0]

    articles = articles.exclude(pk=article.pk) # [:5] # limit 5?
    navitems = NavigationItem.objects.all()

    return render_to_response('blog.html', {'article': article,
                                            'articles': articles,
                                            'navitems': navitems, })

def contact(request):
    TO_EMAIL = ''
    FROM_EMAIL = ''
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
    page = Page.objects.get(slug='contact') # not very resilient, I know...
    return render_to_response('contact.html', {'form': form, 'page': page,
                                               'navitems': navitems, },
                              context_instance=RequestContext(request))


def g_path(request,g_id=None):
    if g_id == None:
        return render_to_response('empty.html')
    graphic = Graphic.objects.get(pk=g_id)
    return render_to_response('empty.html', {'message': graphic.to_path(), })
