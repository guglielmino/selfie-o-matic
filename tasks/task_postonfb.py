import sys, os
import time

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

import cv2
from cv2 import VideoCapture
import numpy as np
from PIL import Image

import logging
import settings

from image_lib import fadein, create_empty_image, overlay_pil_image_pi
from task_common import TaskFrameProcessorBase

class PostOnFbTask(TaskFrameProcessorBase):
	WAIT_SECONDS = 3
	_is_completed = False
	start_time = None
	like_image = Image.open('res/images/fb_like.png')
	_overlay = None
	
	def __init__(self, ctx):
		TaskFrameProcessorBase.__init__(self, ctx)
		self._is_completed = False


	def process_frame(self, frame):
		if self.start_time is None:
			self.start_time = time.time()

		diff_time = int(round(time.time() - self.start_time))
		if diff_time < self.WAIT_SECONDS:
			self._overlay = overlay_pil_image_pi(self.device_ctx.camera, self.like_image)  
		else:
			self.device_ctx.camera.remove_overlay(self._overlay)
			self._is_completed = True

		return frame


	def is_completed(self):
		return self._is_completed