"""Module of utilities to assist with IATI Standard views."""
from celery.result import AsyncResult
from iati_standard.tasks import start_update_task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def on_update_request(request, *args, **kwargs):
    """Schedule update task given URL POST."""
    repo = request.POST.get('repo')
    type_to_update = request.POST.get('type-to-update')
    tag = request.POST.get('live_tag')
    error = None

    if not repo:
        error = 'Error: repo field must be a valid URL'
        return JsonResponse({
            'is_valid': False,
            'error': error,
            'message_class': 'warning',
        })

    if not tag:
        error = 'Error: tag must be selected for data transfer'
        return JsonResponse({
            'is_valid': False,
            'error': error,
            'message_class': 'warning',
        })

    result = start_update_task.delay(repo, tag=tag, type_to_update=type_to_update)

    return JsonResponse({
        'is_valid': True,
        'error': error,
        'message_class': 'success',
        'task_id': result.id,
    })


@csrf_protect
def get_update_progress(request, *args, **kwargs):
    """Get update progress given POST request."""
    result = AsyncResult(request.POST.get('task_id'))
    info = str(result.info)
    message_class = 'success'

    if result.state == 'FAILURE':
        message_class = 'error'

    return JsonResponse({
        'state': result.state,
        'info': info,
        'message_class': message_class,
    })
