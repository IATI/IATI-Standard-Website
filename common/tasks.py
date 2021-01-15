"""Module for Celery tasks."""
from celery import shared_task


@shared_task()
def multiplication_test(x, y):
    """Simple test of mulitiplication using Celery."""
    return x * y
