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

from fb import FacebookHelper
from consts import *


class SnapShotTask(TaskBase):

    '''
    Salvataggio della foto
    '''

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        picture = None

        logging.debug("-- SnapShotTask::execute")

        if "STILL_IMAGE" in self.device_ctx.custom_data:
            picture = self.device_ctx.custom_data["STILL_IMAGE"]
        else:
            stream = io.BytesIO()
            self.device_ctx.camera.capture(
                stream, use_video_port=True, format='jpeg')
            picture = Image.open(stream)

        self.__save_image(picture)

        self._is_completed = True

    def is_completed(self):
        return self._is_completed

    def __save_image(self, frame):
        image_file_name = LOCAL_IMAGE_PATTERN.format(int(time.time()))
        logging.debug("-- SAVING IMAGE TO {0}".format(image_file_name))
        # Gestione HFLIP
        if self.config_manager.getValue(SettingsConsts.KEY_HFLIP_IMAGE):
            logging.debug("-- FLIPPING IMAGE")
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)

        # Watermark della foto
        watermark_image = self.config_manager.getValue(
            SettingsConsts.KEY_WATERMARK_IMAGE)
        if watermark_image and watermark_image.strip():
            logging.debug("-- WATERMARKING IMAGE")
            try:
                frame = watermark_image(
                    frame, Image.open(watermark_image))

            except:
                logging.error(traceback.format_exc())

        frame.save(image_file_name, "JPEG")
        self.device_ctx.custom_data['SNAPSHOT_FILENAME'] = image_file_name
