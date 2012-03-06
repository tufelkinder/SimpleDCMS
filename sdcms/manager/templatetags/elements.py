from sdcms.manager.models import *
from django import template
register = template.Library()

def elem(obj):
    try:
        return Element.objects.get(name=obj).content
    except:
        return ''


def thumb(obj):
    try:
        return Photo.objects.get(name=obj).thumb
    except:
        return ''


def photo(obj):
    try:
        return Photo.objects.get(name=obj).image
    except:
        return ''
