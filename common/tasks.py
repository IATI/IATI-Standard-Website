"""Module for Celery tasks."""
from celery import shared_task


@shared_task()
def multiplication_test(x, y):
    """Test multiplication using Celery."""
    return x * y
