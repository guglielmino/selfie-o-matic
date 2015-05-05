# coding=utf-8

# Progetto: Selfie-O-Matic

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

import thread

from fb import post_image

import logging
import settings

from image_lib import overlay_image, fadein, create_empty_image

from tasks.task_countdown import CountdownTask
from tasks.task_fadetowhite import FadeToWhiteTask
from tasks.task_snapshot import SnapShotTask
from tasks.task_postonfb import PostOnFbTask

__author__ = "Fabrizio Guglielmino"


class SelfieOMatic(object):
	_is_running = False
	# TODO: Coda di frame processors
	_processors = []


	def __init__(self, device=0):

		self.camera = None
		self.cap = None
 		try:
			self.camera = PiCamera()

			self.camera.framerate = 32
			self.rawCapture = PiRGBArray(camera)
			time.sleep(0.1)
		except:
			self.cap = cv2.VideoCapture(device)


	def run(self):
		self._is_running = True
		while self._is_running:
			frame = self.__get_frame()
			self.__process_input()
			frame = self.__process_frame(frame)
			self.__show_frame(frame)
			time.sleep(0.05)


	def cleanup(self):
		if self.cap :
			self.cap.release()
		cv2.destroyAllWindows()


	def __get_frame(self):
		frame = None
		if self.camera:
			img  = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
			frame = img.next().array
		else:
			ret, frame = self.cap.read()
		return frame

	def __process_input(self):
		key = cv2.waitKey(100)
		if key == ord('q'):
			self._is_running = False
		elif key == ord('s'):

			processor = CountdownTask()
			self._processors.append(processor)

			fade = FadeToWhiteTask()
			self._processors.append(fade)

			snap = SnapShotTask()
			self._processors.append(snap)

			postfb = PostOnFbTask()
			self._processors.append(postfb)


	def __process_frame(self, frame):
		if len(self._processors) > 0:
			processor = self._processors[0]
			if processor.is_completed():
				self._processors.remove(processor)
			else:
				frame = processor.process_frame(frame)
		return frame

	def __show_frame(self, frame):
		cv2.imshow(settings.APP_NAME, frame)
		if self.camera:
			self.rawCapture.truncate(0)




if __name__ == '__main__':

	selfie = SelfieOMatic()
	selfie.run()
	selfie.cleanup()
