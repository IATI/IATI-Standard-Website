import requests
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .forms import ContactForm
from .zendeskhelper import generate_ticket


class ContactFormMixin(models.Model):
    """Abstract mixin class to provide contact form functionality to page classes."""

    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        """Overwrite context to intercept POST requests to pages on this template and pass them to Zendesk API.
        """
        context = super().get_context(request, *args, **kwargs)
        context['form'] = ContactForm()
        form_success = False

        if request.method == 'POST':
            context['form'] = form = ContactForm(request.POST)
            if form.is_valid():
                ticket = generate_ticket(request, form)
                if ticket:
                    form_success = True  # TODO: remove
                    # response = requests.post(settings.ZENDESK_REQUEST_URL, json=ticket)
                    # if response.status_code == 201:
                    #     form_success = True
                else:
                    form.add_error(None, _('Sorry, something went wrong submitting your query. Please try again later.'))
                context['form_success'] = form_success
        return context
