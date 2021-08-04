from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from snowpenguin.django.recaptcha3.widgets import ReCaptchaHiddenInput
from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """A form class for a simple contact form."""

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
        error_messages={
            'required': _('This field is required.'),
            'invalid': _('Enter a valid email address.'),
        }
    )
    query = forms.CharField(
        label=_('How can we help you?'),
        widget=forms.Textarea(
            attrs={
                'rows': 'auto',
                'cols': 'auto',
            }
        ),
        error_messages={
            'required': _('This field is required.'),
        }
    )
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput(attrs={'is_hidden': True}))
