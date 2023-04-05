from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "name",
            "email",
            "telephone",
            "text"
        )
