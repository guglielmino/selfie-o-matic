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

class SnapShotTask(TaskFrameProcessorBase):
	'''
	Salvataggio della foto
	'''
	STILL_FRAME_SECONDS = 3
	still_frame = None
	start_time = None

	def init(self):
		self._is_completed = False
	
	def process_frame(self, frame):
		if self.still_frame is None:
			self.still_frame = frame
		if self.start_time is None:
			self.start_time = time.time()


		diff_time = int(round(time.time() - self.start_time))
		print "diff_time {0}".format(diff_time)
		if diff_time < self.STILL_FRAME_SECONDS:
			frame = self.still_frame
		else:
			self.__save_image(self.still_frame)

		return frame

	def is_completed(self):
		return self._is_completed

	def __save_image(self, frame):
		image_file_name = '/tmp/snapshot{0}.jpg'.format(int(time.time()))
		res = cv2.imwrite(image_file_name, frame)
		self._is_completed = True

