import sys
import os
import time
import traceback

import logging

from pushetta import Pushetta
from task_common import TaskBase
from consts import *


class PushettaTask(TaskBase):

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        try:
            p = Pushetta(self.config_manager.getValue(
                SettingsConsts.KEY_PUSHETTA_API_KEY))
            p.pushMessage(self.config_manager.getValue(SettingsConsts.KEY_PUSHETTA_CHANNEL),
                          self.config_manager.getValue(SettingsConsts.KEY_PUSHETTA_MESSAGE))
        except:
            logging.error(traceback.format_exc())

        self._is_completed = True

    def is_completed(self):
        return self._is_completed
