from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your name'),
            }
        ),
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('your.email@address.com'),
            }
        ),
    )
    query = forms.CharField(
        label=_('Query'),
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Your query'),
            }
        ),
    )
