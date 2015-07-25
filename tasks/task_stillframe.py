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

from task_common import TaskBase
from image_lib import overlay_pil_image_pi, watermark_image

from fb import *


class StillFrameTask(TaskBase):

    '''
    Salvataggio della foto
    '''
    STILL_FRAME_SECONDS = 4
    still_frame = None
    start_time = None
    _overlay = None

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        if self.still_frame is None:
            stream = io.BytesIO()
            self.device_ctx.camera.capture(
                stream, use_video_port=True, format='jpeg')
            self.still_frame = Image.open(stream)
            self._overlay = overlay_pil_image_pi(
                self.device_ctx.camera, self.still_frame)
            self.device_ctx.custom_data["STILL_IMAGE"] = self.still_frame

        if self.start_time is None:
            self.start_time = time.time()

        diff_time = int(round(time.time() - self.start_time))

        if diff_time >= self.STILL_FRAME_SECONDS:
            if self._overlay is not None:
                self.device_ctx.camera.remove_overlay(self._overlay)
            self._is_completed = True

    def is_completed(self):
        return self._is_completed
