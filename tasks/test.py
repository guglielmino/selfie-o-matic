# coding=utf-8

import unittest
import sys
import os
from mock import Mock
from mock import MagicMock

testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from fb import *

import settings
from config_manager import ConfigManager
from task_telegram import TelegramTask


class DeviceContext(object):
    camera = None
    cap = None
    custom_data = {}

    def __init__(self, camera, cap):
        self.camera = camera


class TestTelegramTask(unittest.TestCase):
    __configManager = None

    def setUp(self):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        self.__configManager = ConfigManager(cfg_path + '/cfg/test.cfg')
        # Mocking dei metodi del ConfigManager per il test
        self.__configManager.getValue = MagicMock(
            return_value='99016074:AAEpIpAPSCMPYIGQ_j-ziavCyqtihVJTSH0')

    # def test_send_facebook_url(self):
    #     ctx = DeviceContext(None, None)
    #     image_file_name = '/home/pi/Desktop/image.gif'
    #     status = post_on_album(image_file_name, settings.FB_ALBUM_ID)
    #     if 'post_id' in status:
    #         post_info = get_object_info(status['post_id'])
    #         if 'picture' in post_info:
    #             ctx.custom_data["FB_IMAGE_URL"] = post_info['picture']

    #             token = self.__configManager.getValue('TELEGRAM_TOKEN')
    #             print "Using token {0}".format(token)

    # ctx.custom_data['FB_IMAGE_URL'] = 'https://scontent.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/s130x130/11015428_1036887229669178_364442233635440797_n.jpg?oh=d817a1f6166facbda61779d0b2dee65f&oe=565913F7'
    #             telegram = TelegramTask(ctx, self.__configManager)
    #             telegram.execute()
    #             self.assertTrue(True)

    def test_send_physical_file(self):
        ctx = DeviceContext(None, None)
        image_file_name = '/usr/share/scratch/Media/Costumes/Animals/rabbit1.png'
        ctx.custom_data['SNAPSHOT_FILENAME'] = image_file_name
        token = self.__configManager.getValue('TELEGRAM_TOKEN')
        print "Using token {0}".format(token)

        telegram = TelegramTask(ctx, self.__configManager)
        telegram.execute()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
