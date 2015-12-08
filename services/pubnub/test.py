# coding=utf-8

import unittest
import requests
import time
from pubnubclient import *

import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


def callback(message):
    print "callback {0}".format(message)


class TestPubNubClient(unittest.TestCase):

    def setUp(self):
        self.pClient = PubNubClient('00000aa',
                                    "{publish_key}",
                                    "{sub_key}")

    def test_pub(self):
        self.pClient.on('config', callback)
        self.pClient.emit('config', 'test')
        self.pClient.emit('test', 'test')
        time.sleep(3)
        print "DONE"

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
