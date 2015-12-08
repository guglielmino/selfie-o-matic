# coding=utf-8

import unittest
import sys
import os
from mock import MagicMock

testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from config_manager import ConfigManager


class DeviceContext(object):
    camera = None
    cap = None
    custom_data = {}

    def __init__(self, camera, cap):
        self.camera = camera


class TestTask(unittest.TestCase):
    __configManager = None

    def setUp(self):
        pass

    def test_method(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
