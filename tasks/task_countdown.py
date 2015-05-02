
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

from image_lib import overlay_image
from task_common import TaskFrameProcessorBase

class CountdownTask(TaskFrameProcessorBase):
	'''
	Overlay del countdown
	'''
	start_time = None
	_is_completed = False

	counters = [
	 			cv2.imread('res/images/3.png'),
	 			cv2.imread('res/images/2.png'),
	 			cv2.imread('res/images/1.png') 
               ]

	def init(self):
		self._is_completed = False


	def process_frame(self, frame):
		if self.start_time is None:
			self.start_time = time.time()

		diff_time = int(round(time.time() - self.start_time))

		if diff_time < 3:
			img = self.counters[diff_time]
			frame = overlay_image(frame, img)
		else:
			self._is_completed = True

		return frame

	def is_completed(self):
		return self._is_completed
