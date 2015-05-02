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

import logging
import settings

from image_lib import overlay_image, fadein, create_empty_image
from task_common import TaskFrameProcessorBase

class PostOnFbTask(TaskFrameProcessorBase):
	WAIT_SECONDS = 3
	_is_completed = False
	start_time = None
	like_image = cv2.imread('res/images/fb_like.png')
	
	def init(self):
		self._is_completed = False


	def process_frame(self, frame):
		if self.start_time is None:
			self.start_time = time.time()

		diff_time = int(round(time.time() - self.start_time))
		if diff_time < self.WAIT_SECONDS:
			frame = overlay_image(frame, self.like_image)
		else:
			self._is_completed = True

		return frame


	def is_completed(self):
		return self._is_completed