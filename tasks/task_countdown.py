
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
from PIL import Image

from image_lib import overlay_image, overlay_np_image_pi, overlay_pil_image_pi
from task_common import TaskFrameProcessorBase

class CountdownTask(TaskFrameProcessorBase):
	'''
	Overlay del countdown
	'''
	start_time = None
	_is_completed = False
	_running_img = None
	_overlay = None

	counters = [
	 			cv2.imread('res/images/3.png'),
	 			cv2.imread('res/images/2.png'),
	 			cv2.imread('res/images/1.png') 
               ]

	pil_img = [
				Image.open('res/images/3.png'),
				Image.open('res/images/2.png'),
				Image.open('res/images/1.png')
				]



	def __init__(self, ctx):
		TaskFrameProcessorBase.__init__(self, ctx)
		self._is_completed = False


	def process_frame(self, frame):
		if self.start_time is None:
			self.start_time = time.time()

		diff_time = int(round(time.time() - self.start_time))

		if diff_time < 3:
			img = self.counters[diff_time]
			

			if self.device_ctx.camera is None:
				frame = overlay_image(frame, img)
			else:
				if self._running_img != self.pil_img[diff_time]:
					if self._overlay is not None:
						self.device_ctx.camera.remove_overlay(self._overlay)

					self._running_img = self.pil_img[diff_time]
					self._overlay = overlay_pil_image_pi(self.device_ctx.camera, self._running_img, (640, 480))
		else:
			self._is_completed = True

		return frame

	def is_completed(self):
		return self._is_completed
