import sys, os
import time


import logging
import settings

from pushetta import Pushetta
from task_common import TaskBase


class PushettaTask(TaskBase):

    def __init__(self, ctx):
        TaskBase.__init__(self, ctx)
        self._is_completed = False

    def execute(self):
        p=Pushetta(settings.PUSHETTA_API_KEY)
        p.pushMessage(settings.PUSHETTA_CHANNEL, "WOW! Another snapshot in Self-O-Matic history!")
        self._is_completed = True
        

    def is_completed(self):
        return self._is_completed

