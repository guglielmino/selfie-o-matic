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

from image_lib import overlay_image, fadein, create_empty_image, create_empty_image_pil
from task_common import TaskFrameProcessorBase

class FadeToWhiteTask(TaskFrameProcessorBase):
	still_frame = None
	white_image = None
	_is_completed = False
	_fade_value = 6
	_iternal_create_empty_image = None
	_overlay = None
	
	def __init__(self, ctx):
		TaskFrameProcessorBase.__init__(self, ctx)
		self._is_completed = False
		if self.device_ctx.camera is None:
			_iternal_create_empty_image = create_empty_image
		else:
			_iternal_create_empty_image = create_empty_image_pil


	def process_frame(self, frame):
		if self.still_frame is None:
			self.still_frame = frame

		if self.white_image is None:
			height, width = frame.shape[:2]
			self.white_image = _iternal_create_empty_image(height, width, (255,255,255))
		
		if self.device_ctx.camera is None:
			frame = fadein(self.still_frame, self.white_image, self._fade_value)

			self._fade_value = self._fade_value + 3

			if self._fade_value > 10:
				self._is_completed = True
		else:
			if self._overlay is None:
				self._overlay = camera.add_overlay(self.white_image.tostring(), size=self.white_image.size, layer=3, alpha=self._fade_value )
			
			self._overlay.alpha = self._overlay.alpha + 10
			if self._fade_value >= 255:
				self._is_completed = True


		return frame


	def is_completed(self):
		return self._is_completed