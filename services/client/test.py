# coding=utf-8

import unittest
import requests
from ws_client import *


class TestWsClient(unittest.TestCase):

    def setUp(self):
        pass

    def test_unreachable_url(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            client = WsClient("http://localhost:1234")
            client.get_config("4567")


if __name__ == '__main__':
    unittest.main()
