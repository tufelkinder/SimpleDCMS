from django import forms
from django.forms import ModelForm
from sdcms.manager.models import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
