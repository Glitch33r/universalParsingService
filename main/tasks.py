from __future__ import absolute_import, unicode_literals

import json
import logging
import datetime

from celery import shared_task

from main.spider.core import Program
from .models import *

db_logger = logging.getLogger('db')


@shared_task
def unit_task(_id):
    start = datetime.datetime.now()
    unit_code = UnitCode.objects.filter(unit_id=_id)[0].code
    program = Program(_id, unit_code)
    program.run()
    db_logger.info(f'Data saved|{_id}')
    UnitData.objects.create(data=json.dumps(program.variables), unit_id=_id)
    exec_time = datetime.datetime.now() - start
    db_logger.info(f'Execution program time: {exec_time}|{_id}')
