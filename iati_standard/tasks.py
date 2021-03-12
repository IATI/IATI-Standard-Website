"""Module for tasks."""
from __future__ import absolute_import, unicode_literals
from github import GithubException
from iati_standard.data import update_or_create_tags


def start_update_task(task, repo, tag=None, type_to_update=None):
    """Start the updating task."""
    try:
        return update_or_create_tags(task, repo, tag, type_to_update)

    except GithubException as e:
        error = ('GitHub error: %s. Documentation URL: %s' %
                 (e._GithubException__data['message'], e._GithubException__data['documentation_url']))
        task.update_state(
            state='ERROR',
            meta=error
        )
        raise Exception(error)

    except Exception as e:
        error = '%s' % e
        task.update_state(
            state='ERROR',
            meta=error
        )
        raise Exception(error)
