import json

from django.http import HttpResponse

from .spider.utils import Function
from .tasks import *
from django.shortcuts import redirect, render

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def index(request):
    return render(request, 'index.html')


def run_bot(request):
    print(request.GET.dict())
    print(request.GET.get('x'), request.GET.get('y'))
    request.user.profile.tasks.add(create_periodic_task(request.GET.get('x'), request.GET.get('y')))
    # run_bot_task.delay(request.GET.get('x'), request.GET.get('y'))


def create_periodic_task(a, b):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS
    )

    p_task = PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name=f'run_bot_task_{a}_{b}',  # simply describes this periodic task.
        task='main.tasks.run_bot_task',  # name of task.
        args=json.dumps([a, b]),
    )
    return p_task


def dashboard(request):
    return render(request, 'default/dashboard.html')


def faq_page(request):
    data = []
    for cls in all_subclasses(Function):
        data.append(cls().explanation())

    return render(request, 'default/faq.html', {'data': data})


def support_page(request):
    pass
