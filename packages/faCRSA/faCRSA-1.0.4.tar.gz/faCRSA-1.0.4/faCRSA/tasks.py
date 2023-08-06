#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from huey import CancelExecution
from huey.signals import SIGNAL_ERROR

from task_queue import huey

@huey.task()
def submit_task(uid, tid):
    try:
        web_action(uid, tid)
    except (PermissionError, FileExistsError, IndexError, KeyError, NameError) as e:
        raise CancelExecution()

@huey.signal()
def print_signal_args(signal, task, exc=None):
    if signal == SIGNAL_ERROR:
        print('%s - %s - exception: %s' % (signal, task.id, exc))
    else:
        print('%s - %s' % (signal, task.id))


from facrsa_code.library.analysis.main import web_action
