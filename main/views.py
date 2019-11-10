import json

from .tasks import *
from django.shortcuts import redirect, render

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def index(request):
    return render(request, 'index.html')


def run_bot(request):
    print(request.GET.dict())
    # run_bot_task.delay(request.GET.get('x'), request.GET.get('y'))
    create_periodic_task(request.GET.get('x'), request.GET.get('y'))


def create_periodic_task(a, b):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS
    )

    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='run_bot_task_' + a + b,  # simply describes this periodic task.
        task='upt_v2.tasks.run_bot_task',  # name of task.
        args=json.dumps([a, b]),
    )


def index(request):
    return render(request, 'index.html')
