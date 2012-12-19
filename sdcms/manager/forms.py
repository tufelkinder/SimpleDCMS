from django import forms
from django.forms import ModelForm
from manager.models import *


class ContactForm(ModelForm):
    class Meta:
        model = Contact
