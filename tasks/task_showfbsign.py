import time

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

from PIL import Image

from image_lib import overlay_pil_image_pi
from task_common import TaskBase

class ShowFbSignTask(TaskBase):
    '''
    Show FB Like image (real post on fb is made server side)
    '''

    WAIT_SECONDS = 3
    _is_completed = False
    start_time = None
    like_image = Image.open('res/images/fb_like.png')
    _overlay = None

    def __init__(self, ctx, configManager):
        TaskBase.__init__(self, ctx, configManager)
        self._is_completed = False

    def execute(self):
        if self.start_time is None:
            self.start_time = time.time()

        diff_time = int(round(time.time() - self.start_time))
        if diff_time < self.WAIT_SECONDS:
            if not self._overlay:
                self._overlay = overlay_pil_image_pi(
                    self.device_ctx.camera, self.like_image)
        else:
            if self._overlay:
                self.device_ctx.camera.remove_overlay(self._overlay)
            self._is_completed = True

    def is_completed(self):
        return self._is_completed
