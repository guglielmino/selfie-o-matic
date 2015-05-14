import time

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass


import logging
import settings
from PIL import Image

from image_lib import overlay_pil_image_pi
from task_common import TaskBase


class CountdownTask(TaskBase):
    '''
    Task for countdown overlay
    '''
    start_time = None
    _is_completed = False
    _running_img = None
    _overlay = None

    pil_img = [
        Image.open('res/images/3.png'),
        Image.open('res/images/2.png'),
        Image.open('res/images/1.png')
    ]


    def __init__(self, ctx):
        TaskBase.__init__(self, ctx)
        self._is_completed = False


    def execute(self):
        if self.start_time is None:
            self.start_time = time.time()

        diff_time = int(round(time.time() - self.start_time))

        if diff_time < 3:
            if self.device_ctx.camera:
                if self._running_img != self.pil_img[diff_time]:
                    self._running_img = self.pil_img[diff_time]

                    if self._overlay is not None:
                        self.device_ctx.camera.remove_overlay(self._overlay)
                    self._overlay = overlay_pil_image_pi(self.device_ctx.camera, self._running_img)
        else:
            if self._overlay is not None:
                self.device_ctx.camera.remove_overlay(self._overlay)
            self._is_completed = True


    def is_completed(self):
        return self._is_completed
