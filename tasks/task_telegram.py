# coding=utf-8

import time

import telegram
import logging
from config_manager import ConfigManager

from task_common import TaskBase


class TelegramTask(TaskBase):
    _cfgManager = None

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        if 'SNAPSHOT_FILENAME' in self.device_ctx.custom_data:
            snaphot_file = self.device_ctx.custom_data['SNAPSHOT_FILENAME']

            telegram_token = str(
                self.config_manager.getValue('TELEGRAM_TOKEN'))
            bot = telegram.Bot(token=telegram_token)

            chat_ids = set()
            for update in bot.getUpdates():
                chat_id = update.message.chat_id
                chat_ids.add(chat_id)

            for chat_id in chat_ids:
                # Invio di una foro (url)
                bot.sendPhoto(chat_id=chat_id, photo=open(snaphot_file, 'rb'),)

        else:
            print("-- NO IMAGE URL")
        self._is_completed = True

    def is_completed(self):
        return self._is_completed
