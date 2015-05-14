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
    STILL_FRAME_SECONDS = 2
    still_frame = None
    start_time = None
    _overlay = None

    def __init__(self, ctx):
        TaskBase.__init__(self, ctx)
        self._is_completed = False


    def execute(self):
        if self.still_frame is None:
            stream = io.BytesIO()
            self.device_ctx.camera.capture(stream, use_video_port=True, format='jpeg')
            self.still_frame = Image.open(stream)
            self._overlay = overlay_pil_image_pi(self.device_ctx.camera, self.still_frame)

            self.__save_image(self.still_frame)

        if self.start_time is None:
            self.start_time = time.time()

        diff_time = int(round(time.time() - self.start_time))

        if diff_time >= self.STILL_FRAME_SECONDS:
            if self._overlay is not None:
                self.device_ctx.camera.remove_overlay(self._overlay)
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

		


