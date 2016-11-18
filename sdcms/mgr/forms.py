from __future__ import unicode_literals

from django.forms import ModelForm
from mgr.models import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('date',)
