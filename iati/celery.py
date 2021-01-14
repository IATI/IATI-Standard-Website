"""Module to configure Celery app."""

from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('iati')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Print debug log for Celery requests."""
    print('Request: {0!r}'.format(self.request))
