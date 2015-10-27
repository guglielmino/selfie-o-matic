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

from fb import *
from twitter import *
import dropbox
from consts import *
from image_lib import resize_image_height


class UploadLostTask(TaskBase):
    files_pattern = LOCAL_IMAGE_PATTERN.format('*')
    # Vengono postati i file più vecchi di 30sec per evitare di andare in concorrenza con i processi di
    # creazion e modifica della foto
    age_in_seconds = 10

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

                    fb_posted = False
                    tw_posted = False
                    # Post on FB
                    try:
                        status = post_on_album(
                            image_file, settings.FB_ALBUM_ID)
                        if 'post_id' in status:
                            fb_posted = True
                        else:
                            logging.error(str(status))
                    except:
                        logging.error(traceback.format_exc())

                    # Post on Twitter
                    try:
                        tweet_image(image_file, settings.TW_STATUS_MSG)
                        tw_posted = True
                    except:
                        logging.error(traceback.format_exc())

                    # Upload Dropbox
                    try:
                        # Resize image
                        resized_file = '/tmp/' + os.path.basename(image_file)
                        resize_image_height(image_file, resized_file, 900)

                        client = dropbox.client.DropboxClient(
                            settings.DB_ACCESS_TOKEN)
                        f = open(resized_file, 'rb')
                        response = client.put_file(
                            os.path.basename(resized_file), f)
                        logging.debug("Dropbox {0}".format(response))
                    except:
                        logging.error(traceback.format_exc())

                    if fb_posted or tw_posted:
                        shutil.move(image_file, PUBLISHED_FOLDER)

    def is_completed(self):
        return False
