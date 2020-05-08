"""Module for Celery tasks."""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from github import GithubException
from iati_standard.data import update_or_create_tags


@shared_task(bind=True)
def start_update_task(self, repo, tag=None, guidance_parent_page=None):
    """Start the updating task."""
    try:
        return update_or_create_tags(self, repo, tag, guidance_parent_page)

    except GithubException as e:
        error = ('GitHub error: %s. Documentation URL: %s' %
                 (e._GithubException__data['message'], e._GithubException__data['documentation_url']))
        self.update_state(
            state='ERROR',
            meta={
                'error': error,
                'message_class': 'error',
            },
        )
        raise Exception(error)

    except Exception as e:
        error = '%s' % e
        self.update_state(
            state='ERROR',
            meta={
                'error': error,
                'message_class': 'error',
            },
        )
        raise Exception(error)
