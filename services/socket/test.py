# coding=utf-8

import unittest
import requests
from socketclient import *

import logging
logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class TestSocketClient(unittest.TestCase):

    def setUp(self):
        pass

    def test_unreachable_url(self):
        self._socketClient = SocketClient(
            "localhost", 1234)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
