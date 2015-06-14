import time
import os
import io
import traceback

from PIL import Image
import threading

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

import logging
import settings

from task_common import TaskBase
from image_lib import overlay_pil_image_pi, watermark_image

from fb import *


class SnapShotTask(TaskBase):
    '''
    Salvataggio della foto
    '''

    def __init__(self, ctx):
        TaskBase.__init__(self, ctx)
        self._is_completed = False


    def execute(self):
        picture = None

        if "STILL_IMAGE" in self.device_ctx.custom_data:
            picture = self.device_ctx.custom_data["STILL_IMAGE"]
        else:
            stream = io.BytesIO()
            self.device_ctx.camera.capture(stream, use_video_port=True, format='jpeg')
            picture = Image.open(stream)

        self.__save_image(picture)

        self._is_completed = True


    def is_completed(self):
        return self._is_completed

    def __save_image(self, frame):
        image_file_name = '/tmp/snapshot{0}.jpg'.format(int(time.time()))

        # Gestione HFLIP
        if settings.HFLIP_IMAGE:
            logging.debug("-- FLIPPING IMAGE")
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)

        # Watermark della foto
        if settings.WATERMARK_IMAGE and settings.WATERMARK_IMAGE.strip():
            logging.debug("-- WATERMARKING IMAGE")
            try:
                frame = watermark_image(frame, Image.open(settings.WATERMARK_IMAGE))
            except:
                logging.error(traceback.format_exc())

        frame.save(image_file_name, "JPEG")

        # Post on FB
        try:
            status = post_on_album(image_file_name, settings.FB_ALBUM_ID)
            if 'post_id' in status:
                os.remove(image_file_name)
            else:
                logging.error(str(status))
        except:
            logging.error(traceback.format_exc())



		


