# coding=utf-8

# Progetto: Selfie-O-Matic
# Descrizione: Task che gestisce l'upload sui social delle immagini


import os
import io
import traceback
import sys
from glob import glob
import time
import shutil

from task_common import TaskBase

import logging
import settings


from fb import FacebookHelper
from twitter import TwitterHelper

import dropbox
from consts import *


class UploadLostTask(TaskBase):
    files_pattern = LOCAL_IMAGE_PATTERN.format('*')
    # Vengono postati i file più vecchi di 30sec per evitare di andare in concorrenza con i processi di
    # creazion e modifica della foto
    age_in_seconds = 10

    _fb_helper = None
    _tw_helper = None

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._fb_helper = FacebookHelper(app_id=configManager.getValue(SettingsConsts.KEY_FB_APP_ID),
                                         access_token=configManager.getValue(SettingsConsts.KEY_FB_ACCESS_TOKEN))

        self._tw_helper = TwitterHelper(consumer_key=configManager.getValue(SettingsConsts.KEY_TW_CONSUMER_KEY),
                                        consumer_secret=configManager.getValue(
                                            SettingsConsts.KEY_TW_CONSUMER_SECRET),
                                        access_token=configManager.getValue(
                                            SettingsConsts.KEY_TW_ACCESS_TOKEN),
                                        access_token_secret=configManager.getValue(SettingsConsts.KEY_TW_ACCESS_TOKEN_SECRET))

    def execute(self):
        logging.debug("-- CHECK LOST POST")
        images = glob(self.files_pattern)
        now = time.time()
        for image_file in images:

            if os.stat(image_file).st_mtime < now - self.age_in_seconds:
                if os.path.isfile(image_file):
                    logging.debug("-- RECOVERY POST {0}".format(image_file))

                    fb_posted = False
                    tw_posted = False

                    # Post on FB

                    try:
                        status = self._fb_helper.post_on_album(
                            image_file_name, str(
                                self.config_manager.getValue(SettingsConsts.KEY_FB_ALBUM_ID)))
                        if 'post_id' in status:
                            post_info = self._fb_helper.get_object_info(
                                status['post_id'])
                            if 'picture' in post_info:
                                self.device_ctx.custom_data[
                                    "FB_IMAGE_URL"] = post_info['picture']
                                fb_posted = True
                        else:
                            logging.error(str(status))
                    except:
                        logging.error(traceback.format_exc())

                    # Post on Twitter
                    try:
                        self._tw_helper.tweet_image(
                            image_file, settings.TW_STATUS_MSG)
                        tw_posted = True
                    except:
                        logging.error(traceback.format_exc())

                    # Upload Dropbox
                    try:
                        client = dropbox.client.DropboxClient(
                            self.config_manager.getValue(SettingsConsts.KEY_DB_ACCESS_TOKEN))
                        f = open(image_file, 'rb')
                        response = client.put_file(
                            os.path.basename(image_file), f)
                        logging.debug("Dropbox {0}".format(response))
                    except:
                        logging.error(traceback.format_exc())

                    if fb_posted or tw_posted:
                        shutil.move(image_file, PUBLISHED_FOLDER)

    def is_completed(self):
        return False
