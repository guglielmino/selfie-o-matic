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

class FadeToWhiteTask(TaskFrameProcessorBase):
	still_frame = None
	white_image = None
	_is_completed = False
	_fade_value = 6

	
	def __init__(self, ctx):
		TaskFrameProcessorBase.__init__(self, ctx)
		self._is_completed = False


	def process_frame(self, frame):
		if self.still_frame is None:
			self.still_frame = frame

		if self.white_image is None:
			height, width = frame.shape[:2]
			self.white_image = create_empty_image(height, width, (255,255,255))
		
		frame = fadein(self.still_frame, self.white_image, self._fade_value)
		self._fade_value = self._fade_value + 3

		if self._fade_value > 10:
			self._is_completed = True

		return frame


	def is_completed(self):
		return self._is_completed