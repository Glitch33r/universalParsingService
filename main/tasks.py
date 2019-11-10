from __future__ import absolute_import, unicode_literals

import pytz
from celery import shared_task
from upt_v2.celery import app
import requests
import bs4
from .models import *

# Create your views here.


@shared_task
def run_bot_task(x, y):
    z = int(x) + int(y)
    print(z)
    data(text=str(z)).save()
