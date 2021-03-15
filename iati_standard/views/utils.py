"""Module of utilities to assist with IATI Standard views."""
import threading
from iati_standard.tasks import start_update_task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from iati_standard.models import SyncTaskResult


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
    task = SyncTaskResult.objects.create()
    threading.Thread(target=start_update_task, args=[task, repo], kwargs={'tag': tag, 'type_to_update': type_to_update}).start()
    return JsonResponse({
        'is_valid': True,
        'error': error,
        'message_class': 'success',
        'task_id': task.task_id,
    })


@csrf_protect
def get_update_progress(request, *args, **kwargs):
    """Get update progress given POST request."""
    result = SyncTaskResult.objects.get(task_id=request.POST.get('task_id'))
    info = str(result.info)
    state = result.state
    message_class = 'success'

    if state in ['FAILURE', 'ERROR']:
        message_class = 'error'
        result.delete()

    if state == 'SUCCESS':
        result.delete()

    return JsonResponse({
        'state': state,
        'info': info,
        'message_class': message_class,
    })
