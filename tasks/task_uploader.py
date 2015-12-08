# coding=utf-8

# Progetto: Selfie-O-Matic
# Descrizione: Task che gestisce l'upload sui social delle immagini


import os
import traceback
from glob import glob
import time
import shutil

from task_common import TaskBase
from utility import getserial
from file_uploader import UploaderHelper

import logging
import settings

import dropbox
from consts import *


class UploaderTask(TaskBase):
    files_pattern = LOCAL_IMAGE_PATTERN.format('*')
    # Vengono postati i file più vecchi di x sec per evitare di andare in concorrenza con i processi di
    # creazion e modifica della foto
    age_in_seconds = 10

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)

    def execute(self):
        logging.debug("-- CHECK FILES TO UPLOADS")
        images = glob(self.files_pattern)
        now = time.time()
        for image_file in images:

            if os.stat(image_file).st_mtime < now - self.age_in_seconds:
                if os.path.isfile(image_file):
                    logging.debug("-- UPLOAD OF {0}".format(image_file))

                    posted = False

                    # Upload to Self-O-Matic API
                    posted = self.__upload_on_api(image_file)

                    # Upload Dropbox
                    self.__upload_on_dropbox(image_file)

                    if posted:
                        shutil.move(image_file, PUBLISHED_FOLDER)

    def is_completed(self):
        return False

    def __upload_on_api(self, image_file):
        ret = False
        try:
            uploader = UploaderHelper('http://' + settings.API_HOSTNAME)
            ret = uploader.upload_file(
                '/api/machines/' + getserial() + '/upload', image_file)
        except:
            logging.error(traceback.format_exc())

        return ret

    def __upload_on_dropbox(self, image_file):
        try:
            client = dropbox.client.DropboxClient(
                self.config_manager.getValue(SettingsConsts.KEY_DB_ACCESS_TOKEN))
            f = open(image_file, 'rb')
            response = client.put_file(
                os.path.basename(image_file), f)
            logging.debug("Dropbox {0}".format(response))
        except:
            logging.error(traceback.format_exc())
