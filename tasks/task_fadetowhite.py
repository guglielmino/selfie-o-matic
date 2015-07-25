import sys
import os
import time

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

import logging

from image_lib import create_empty_image_pil, overlay_pil_image_pi
from task_common import TaskBase


class FadeToWhiteTask(TaskBase):
    white_image = None
    _is_completed = False
    _fade_value = 6
    _overlay = None
    _fade_step = 50

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        if self.white_image is None:
            height, width = self.device_ctx.camera.resolution
            self.white_image = create_empty_image_pil(
                height, width, (255, 255, 255))

        if self._overlay is None:
            self._overlay = overlay_pil_image_pi(
                self.device_ctx.camera, self.white_image)
            self._overlay.alpha = 0

        if self._overlay.alpha + self._fade_step < 255:
            self._overlay.alpha = self._overlay.alpha + self._fade_step
        else:
            self.device_ctx.camera.remove_overlay(self._overlay)
            self._is_completed = True

    def is_completed(self):
        return self._is_completed
