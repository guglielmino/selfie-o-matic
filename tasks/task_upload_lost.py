# coding=utf-8

# Progetto: Selfie-O-Matic
# Descrizione: Task che gestisce l'upload su fb delle immagini scorie lasciate in temp
# Quelle che potenzialmente il sistema non è riuscito a postare in
# realtime


import os
import io
import traceback
import sys
from glob import glob
import time


from task_common import TaskBase

import logging
import settings

from fb import *


class UploadLostTask(TaskBase):
    files_pattern = '/tmp/snapshot*.jpg'
    # I file più vecchi di 5 min sono scatti che non sono stati uploatati
    age_in_seconds = 300

    def __init__(self, ctx):
        TaskBase.__init__(self, ctx)

    def execute(self):
        logging.debug("-- CHECK LOST POST")
        images = glob(self.files_pattern)
        now = time.time()
        for image_file in images:

            if os.stat(image_file).st_mtime < now - self.age_in_seconds:
                if os.path.isfile(image_file):
                    logging.debug("-- RECOVERY POST {0}".format(image_file))
                    # Post on FB
                    try:
                        status = post_on_album(
                            image_file, settings.FB_ALBUM_ID)
                        if 'post_id' in status:
                            os.remove(image_file)
                        else:
                            logging.error(str(status))
                    except:
                        logging.error(traceback.format_exc())

    def is_completed(self):
        return False
