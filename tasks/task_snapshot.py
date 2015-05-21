import sys, os
import time
import io
from PIL import Image


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
from image_lib import overlay_image, overlay_np_image_pi, overlay_pil_image_pi

class SnapShotTask(TaskFrameProcessorBase):
	'''
	Salvataggio della foto
	'''
	STILL_FRAME_SECONDS = 3
	still_frame = None
	start_time = None
	_overlay = None

	def __init__(self, ctx):
		TaskFrameProcessorBase.__init__(self, ctx)
		self._is_completed = False
	
	def process_frame(self, frame):
		if self.still_frame is None:
			stream = io.BytesIO()
			camera.capture(stream, format='jpeg')
			self.still_frame = Image.open(stream)
			self.__save_image(self.still_frame)
		if self.start_time is None:
			self.start_time = time.time()



		diff_time = int(round(time.time() - self.start_time))
		print "diff_time {0}".format(diff_time)
		if diff_time < self.STILL_FRAME_SECONDS:
			self._overlay = overlay_pil_image_pi(self.device_ctx.camera, self.still_frame, (640, 480))
		else:
			if self._overlay is not None:
				self.device_ctx.camera.remove_overlay(self._overlay)

		return frame

	def is_completed(self):
		return self._is_completed

	def __save_image(self, frame):
		image_file_name = '/tmp/snapshot{0}.jpg'.format(int(time.time()))
		im.save(image_file_name, "JPEG")
		self._is_completed = True


