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

    _fb_helper = None

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False
        self._fb_helper = FacebookHelper(app_id=configManager.getValue("FB_APP_ID"),
                                         access_token=configManager.getValue("FB_ACCESS_TOKEN"))

    def execute(self):
        picture = None

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

        # Gestione HFLIP
        if self.config_manager.getValue("HFLIP_IMAGE"):
            logging.debug("-- FLIPPING IMAGE")
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)

        # Watermark della foto
        watermark_image = self.config_manager.getValue("WATERMARK_IMAGE")
        if watermark_image and watermark_image.strip():
            logging.debug("-- WATERMARKING IMAGE")
            try:
                frame, Image.open(watermark_image))

            except:
                logging.error(traceback.format_exc())

        frame.save(image_file_name, "JPEG")
        self.device_ctx.custom_data['SNAPSHOT_FILENAME']=image_file_name

        # Post on FB
        try:
            status=self._fb_helper.post_on_album(
                image_file_name, str(
                    self.config_manager.getValue("FB_ALBUM_ID")))
            if 'post_id' in status:
                post_info=self._fb_helper.get_object_info(status['post_id'])
                if 'picture' in post_info:
                    self.device_ctx.custom_data[
                        "FB_IMAGE_URL"] = post_info['picture']
            else:
                logging.error(str(status))
        except:
            logging.error(traceback.format_exc())
