import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm
from .zendeskhelper import generate_ticket

CAPTCHA_FIELD_NAME = 'captcha'
LOW_SCORE = 'score'
FIELD_REQUIRED = 'required'


class ContactFormMixin(models.Model):
    """Abstract mixin class to provide contact form functionality to page classes."""

    class Meta:
        abstract = True

    def post_submission(self, request, context, score=None, suspicious=False):
        """Try generating a ticket and posting a request to Zendesk, update and return the context object."""
        form = context['form']
        ticket = generate_ticket(request, form, score, suspicious)
        if ticket:
            response = requests.post(settings.ZENDESK_REQUEST_URL, json=ticket)
            if response.status_code == 201:
                context['form_success'] = True
            else:
                form.add_error(None, _('Sorry, something went wrong submitting your query. Please try again later.'))
        else:
            form.add_error(None, _('Sorry, something went wrong submitting your query. Please try again later.'))

        if suspicious:
            form.errors.pop(CAPTCHA_FIELD_NAME)

        return context

    def get_context(self, request, *args, **kwargs):
        """Overwrite context to intercept POST requests to pages on this template and pass them to Zendesk API."""
        context = super().get_context(request, *args, **kwargs)
        context['form'] = ContactForm()
        context['form_success'] = False
        context['public_key'] = settings.RECAPTCHA_PUBLIC_KEY

        if request.method == 'POST':
            context['form'] = form = ContactForm(request.POST)

            try:
                # get all the errors
                errors = form.errors.as_data()
                non_captcha_error = False

                # check if we have any non captcha errors, if so let the form return invalid
                for k in errors.keys():
                    if k != CAPTCHA_FIELD_NAME:
                        non_captcha_error = True
                        break

                # remove captcha field required error if present, as it makes no sense (JS disabled edge case)
                if non_captcha_error:
                    form.errors.pop(CAPTCHA_FIELD_NAME)

                # if no non captcha errors, go ahead and check if the field has a bad score or is missing altogether (JS disabled)
                elif form.has_error(CAPTCHA_FIELD_NAME):
                    captcha_errors = errors.get(CAPTCHA_FIELD_NAME)
                    for item in captcha_errors:
                        if item.code == LOW_SCORE or item.code == FIELD_REQUIRED:
                            score = 0.0
                            if item.code == LOW_SCORE:
                                score = item.params['score']

                            return self.post_submission(request, context, score=score, suspicious=True)

            except Exception:
                pass

            if form.is_valid():
                return self.post_submission(request, context)

        return context
