# coding=utf-8

# Progetto: Selfie-O-Matic

import sys
import os
import time
import io
from consts import *

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

try:
    import RPi.GPIO as GPIO
except:
    pass

import cv2

import logging
import settings

from tasks.task_countdown import CountdownTask
from tasks.task_fadetowhite import FadeToWhiteTask
from tasks.task_stillframe import StillFrameTask
from tasks.task_snapshot import SnapShotTask
from tasks.task_postonfb import PostOnFbTask
from tasks.task_pushetta import PushettaTask
from tasks.task_upload_lost import UploadLostTask

from task_manager import TaskManager

from tendo import singleton

__author__ = "Fabrizio Guglielmino"

APP_NAME = "Self-O-Matic"
VERSION = "0.3"


class DeviceContext(object):
    camera = None
    cap = None
    custom_data = {}

    def __init__(self, camera, cap):
        self.camera = camera


class SelfieOMatic(object):
    _is_running = False
    # True quando sta processando una foto
    _is_snap = False

    # TODO: Coda di frame processors
    _processors = []
    _task_manager = TaskManager()
    rawCapture = None
    ctx = DeviceContext(None, None)

    def __init__(self, device=0):

        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='selfie-o-matic.log', level=logging.INFO)

        self.ctx.camera = None

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        try:
            cv2.namedWindow("MainWin")

            self.ctx.camera = PiCamera()
            if settings.HFLIP_IMAGE:
                self.ctx.camera.hflip = True

            self.ctx.camera.framerate = 24
            self.ctx.camera.preview_fullscreen = True
            self.ctx.camera.awb_mode = 'sunlight'
            self.ctx.camera.exposure_mode = 'snow'

            self.ctx.camera.start_preview()
            self.rawCapture = PiRGBArray(self.ctx.camera)
            time.sleep(0.3)

        except:
            logging.error("picamera init failed")

        if not os.path.exists(PUBLISHED_FOLDER):
            os.mkdir(PUBLISHED_FOLDER)

        # Scheduling del task di recupero immagini non uploadate
        upload_lost = UploadLostTask(self.ctx)
        self._task_manager.add_scheduled_task(upload_lost)

    def run(self):
        self._is_running = True
        while self._is_running:
            self.__process_input()
            self.__process_tasks()
            time.sleep(0.05)

    def cleanup(self):
        if self.ctx.camera:
            self.ctx.camera.stop_preview()
            self.ctx.camera.close()
        cv2.destroyAllWindows()

    def __process_input(self):
        key = cv2.waitKey(10)

        if GPIO:
            input_state = GPIO.input(18)
            if input_state == False:
                # Remap
                key = ord('s')

        if key == ord('q'):
            cv2.destroyAllWindows()
            self._is_running = False

        elif key == ord('s'):
            if not self._is_snap:
                self._is_snap = True

                # Snapshot workflow
                countdown = CountdownTask(self.ctx)
                fade = FadeToWhiteTask(self.ctx)
                still = StillFrameTask(self.ctx)
                snap = SnapShotTask(self.ctx)
                postfb = PostOnFbTask(self.ctx)

                # Async snapshot, image processing ad post on fb
                #still.set_on_completed(self.__after_fade_event)

                self._task_manager.add_task(countdown)
                self._task_manager.add_task(fade)
                self._task_manager.add_task(still)
                self._task_manager.add_task(snap)
                self._task_manager.add_task(postfb)

    def __after_fade_event(self, taskmanager):
        # push = PushettaTask(self.ctx)
        # taskmanager.add_async_task(push)
        snap = SnapShotTask(self.ctx)
        taskmanager.add_async_task(snap)

    def __process_tasks(self):
        self._is_snap = self._task_manager.cycle()

if __name__ == '__main__':
    # Gestione della singola istanza
    me = singleton.SingleInstance()
    selfie = SelfieOMatic()
    selfie.run()
    selfie.cleanup()
