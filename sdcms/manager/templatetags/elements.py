from manager.models import *
from django import template
register = template.Library()

# usage: {{ e|elem:"sidebar"|safe }}

@register.filter
def elem(obj,obj2):
    try:
        return Element.objects.get(name=obj2).content
    except:
        return ''


@register.filter
def thumb(obj,obj2):
    try:
        return Photo.objects.get(name=obj2).thumb
    except:
        return ''


@register.filter
def photo(obj,obj2):
    try:
        return Photo.objects.get(name=obj2).image
    except:
        return ''
