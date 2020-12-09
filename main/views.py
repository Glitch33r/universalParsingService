import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import PeriodicTask

from .forms import *
from .spider.utils import Function
from .tasks import *


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'default/dashboard.html')


def faq_page(request):
    funcs = []
    for cls in all_subclasses(Function):
        funcs.append(cls().explanation())

    return render(request, 'default/faq.html', {'data': funcs})


def support_page(request):
    if request.method == 'POST':
        support = SupportForm(request.POST)
        if support.is_valid():
            action = support.save(commit=False)
            action.user = request.user
            action.save()
            messages.success(
                request,
                'Thank you! Your query sent successfully.'
            )
            return redirect(reverse('main:support'))
    else:
        support = SupportForm()

    return render(request, 'default/support.html', {'form': support})


def create_unit_form(request):
    if request.method == 'POST':
        unit = UnitCreateForm(request.POST, prefix='unit')
        code = UnitCodeForm(request.POST, prefix='code')
        if unit.is_valid() and code.is_valid():
            action = unit.save(commit=False)
            action.user = request.user
            code = code.save(commit=False)
            action.save()
            code.unit = action
            code.save()
            messages.success(
                request,
                'Yes! Your unit created successfully.'
            )
            return redirect(reverse('main:list-unit'))
    else:
        unit = UnitCreateForm(prefix='unit')
        code = UnitCodeForm(prefix='code')

    return render(request, 'bot/create_unit.html', {'form_unit': unit, 'form_code': code})


# def create_unit_code_form(request):
#     return render(request, 'bot/create_code.html')


def list_unit(request):
    if request.user.is_superuser:
        values = Unit.objects.all()
    else:
        values = Unit.objects.filter(user=request.user)
    return render(request, 'bot/list_unit.html', {'data': values})


def unit_update(request, pk: int):
    obj = get_object_or_404(Unit, pk=pk)
    unit = UnitFormUpdate(request.POST or None, instance=obj, prefix="unit")

    obj_code = get_object_or_404(UnitCode, unit=obj)
    code = UnitCodeForm(request.POST or None, instance=obj_code, prefix="code")

    if request.method == 'POST':
        if unit.is_valid() and code.is_valid():
            unit.save()
            code.save()
            messages.success(
                request,
                'Unit was updated successfully!'
            )
            return redirect(reverse('main:list-unit'))

    return render(request, 'bot/update_unit.html', {'form_unit': unit, 'form_code': code})


def unit_delete(request, obj_id: int):
    obj = get_object_or_404(Unit, pk=obj_id)
    obj.delete()

    return redirect(reverse('main:list-unit'))


def launch_unit(request):
    user = request.user
    tasks = user.profile.tasks.all()
    return render(request, 'bot/launch_unit.html', {'data': tasks})


def launch_unit_update(request, pk):
    obj = get_object_or_404(PeriodicTask, pk=pk)
    task = PeriodicTaskUpdateForm(request.POST or None, instance=obj, prefix="task")

    obj_cron = get_object_or_404(CrontabSchedule, pk=obj.crontab.pk)
    cron = CrontabForm(request.POST or None, instance=obj_cron, prefix="cron")

    if request.method == 'POST':
        if task.is_valid() and cron.is_valid():
            task.save()
            cron.save()
            messages.success(
                request,
                'Task was updated successfully!'
            )
            return redirect(reverse('main:launch-unit'))

    return render(request, 'bot/launch_task_update_form.html', {'form_task': task, 'form_cron': cron})


@csrf_exempt
def launch_refresh(request):
    if request.is_ajax():
        user = request.user
        tasks = user.profile.tasks.all()
        html = render_to_string('bot/launch_table_part.html', {'data': tasks})
        return HttpResponse(html)


@csrf_exempt
def launch_unit_form(request):
    units = Unit.objects.filter(user=request.user)

    if request.is_ajax():
        unit_id = request.POST.get('id')
        unit = Unit.objects.filter(pk=unit_id)[0]
        crontab = CrontabForm()
        html = render_to_string('bot/launch_part.html', {'value': unit, 'form': crontab})
        return HttpResponse(html)
    elif request.method == 'POST':
        POST = request.POST.copy()
        task_name = POST.pop('task_name')[0]
        task_desc = POST.pop('task_desc')[0]
        unit_id = POST.pop('unit_id')[0]
        crontab = CrontabForm(POST)
        if crontab.is_valid():
            obj_crontab = crontab.save()
            create_periodic_task(request, task_name, task_desc, obj_crontab, unit_id)
            messages.success(
                request,
                'Unit task was added successfully!'
            )
            return redirect(reverse('main:launch-unit'))

    return render(request, 'bot/launch_unit_form.html', {'data': units})


def collected_data(request):
    user_id = request.user
    unit = Unit.objects.filter(user=user_id)
    return render(request, 'bot/collected_data.html', {'data': unit})


def collected_data_show(request, pk):
    unit = Unit.objects.filter(pk=pk)[0]
    values = UnitData.objects.filter(unit_id=unit.id)
    return render(request, 'bot/collected_data_show.html', {'unit': unit, 'data': values})


def create_periodic_task(request, name, description, schedule, unit_id):
    task = PeriodicTask.objects.create(
        crontab=schedule,  # we created this above.
        name=name,  # simply describes this periodic task.
        task='main.tasks.unit_task',  # name of task.
        description=description,
        args=json.dumps(unit_id),
    )
    request.user.profile.tasks.add(task)

    return task
