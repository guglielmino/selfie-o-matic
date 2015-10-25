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

from utility import getserial, getname

from tasks.task_countdown import CountdownTask
from tasks.task_fadetowhite import FadeToWhiteTask
from tasks.task_stillframe import StillFrameTask
from tasks.task_snapshot import SnapShotTask
from tasks.task_postonfb import PostOnFbTask
from tasks.task_pushetta import PushettaTask
from tasks.task_telegram import TelegramTask
from tasks.task_upload_lost import UploadLostTask

from task_manager import TaskManager
from config_manager import ConfigManager
from services.client.ws_client import WsClient
from services.socket.socketclient import SocketClient

__author__ = "Fabrizio Guglielmino"

APP_NAME = "Self-O-Matic"
VERSION = "0.3"
CODENAME = "cloudy"


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

    _task_manager = TaskManager()
    # TODO: Verificare se si può rimuovere rawCapture
    rawCapture = None
    ctx = DeviceContext(None, None)
    # Configuration manager
    _configManager = None

    # Connessione WebSocket
    _socketClient = None

    # Client WebService
    _serviceClient = None

    def __init__(self, device=0):

        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='selfie-o-matic.log', level=logging.DEBUG)

        app_path = os.path.dirname(os.path.abspath(__file__))
        self._configManager = ConfigManager(
            app_path + '/cfg/selfie-o-matic.cfg')

        self.__initSocketClient()
        self.__initServiceClient()

        self.ctx.camera = None

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        try:
            cv2.namedWindow("MainWin")

            self.ctx.camera = PiCamera()
            if self._configManager.getValue("HFLIP_IMAGE"):
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
            print(sys.exc_info()[0])
            print("----")

        if not os.path.exists(PUBLISHED_FOLDER):
            os.mkdir(PUBLISHED_FOLDER)

        # Scheduling del task di recupero immagini da uploadate
        upload_lost = UploadLostTask(self.ctx, self._configManager)
        self._task_manager.add_scheduled_task(upload_lost)

    def __initSocketClient(self):
        try:
            self._socketClient = SocketClient(
                settings.API_HOSTNAME, settings.API_PORT)
            serial = getserial()
            print("REGISTERING SOCKETCLIENT ON {0}".format(serial))
            self._socketClient.emit('register', getserial())
            self._socketClient.on('config_update', self.__on_config_update)
        except:
            self._socketClient = None
            print("Error initialiting Socket.io client")
            print(sys.exc_info()[0])

    def __initServiceClient(self):
        try:
            serial = getserial()
            self._serviceClient = WsClient(
                ''.join(["http://", settings.API_HOSTNAME, ":", str(settings.API_PORT)]))
            self._serviceClient.register_myself(serial, getname())
            # Acquisizione della config storata server side
            configData = self._serviceClient.get_config(serial)
            if configData:
                self.__update_local_config(configData)

        except:
            self._serviceClient = None
            print("Error initialiting web service client")
            print(sys.exc_info()[0])

    def run(self):
        self._is_running = True
        while self._is_running:
            self.__process_input()
            self.__process_tasks()

            if self._socketClient:
                self._socketClient.wait(seconds=0.05)
            else:
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
                countdown = CountdownTask(self.ctx, self._configManager)
                fade = FadeToWhiteTask(self.ctx, self._configManager)
                still = StillFrameTask(self.ctx, self._configManager)
                snap = SnapShotTask(self.ctx, self._configManager)
                postfb = PostOnFbTask(self.ctx, self._configManager)

                # Async snapshot, image processing ad post on fb
                still.set_on_completed(self.__after_fade_event)

                self._task_manager.add_task(countdown)
                self._task_manager.add_task(fade)
                self._task_manager.add_task(still)
                # self._task_manager.add_task(snap)
                self._task_manager.add_task(postfb)

    def __after_fade_event(self, taskmanager):
        push = PushettaTask(self.ctx, self._configManager)
        taskmanager.add_async_task(push)

        snap = SnapShotTask(self.ctx, self._configManager)
        taskmanager.add_async_task(snap)

        telegram = TelegramTask(self.ctx, self._configManager)
        taskmanager.add_async_task(telegram)

    def __process_tasks(self):
        self._is_snap = self._task_manager.cycle()

    def __on_config_update(self, configData):
        print("on_config_update")
        self.__update_local_config(configData)

    def __update_local_config(self, configData):
        for key in configData.keys():
            # Store delle chiavi di config ricevute dal servizio
            self._configManager.setValue(key.upper(), configData[key])
            print("Config {0}={1}".format(key.upper(), configData[key]))


if __name__ == '__main__':

    selfie = SelfieOMatic()
    selfie.run()
    selfie.cleanup()
