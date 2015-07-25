
import unittest
import sys
import os

from services.client.ws_client import WsClient
from config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):

	__configManager = None

	def setUp(self):
		cfg_path = os.path.dirname(os.path.abspath(__file__))
		self.__configManager = ConfigManager(cfg_path + '/cfg/test.cfg')

	def test_read_setting(self):
		res = self.__configManager.getValue("FB_ALBUM_ID")
		self.assertIsNotNone(res)

	def test_write_setting(self):
		res = self.__configManager.setValue("FB_ALBUM_ID", "123")
		self.assertEqual(self.__configManager.getValue("FB_ALBUM_ID"), "123")

	def test_write_many_setting(self):
		res = self.__configManager.setValue("ATTRIB_ONE", "aaa")
		self.assertEqual(self.__configManager.getValue("ATTRIB_ONE"), "aaa")
		res = self.__configManager.setValue("ATTRIB_TWO", "bbb")
		self.assertEqual(self.__configManager.getValue("ATTRIB_TWO"), "bbb")


class TestWsClient(unittest.TestCase):
	def test_ws_client(self):
		client = WsClient("http://admin.self-o-matic.com")
		res = client.register_myself("123", "UNIT TEST MACHINE")
		self.assertTrue(res)


# class TestFB(unittest.TestCase):	

# 	def test_post_on_page(self):

# 		cfg = {
# 		    "page_id"      : "1008802539144314",  
# 		    "access_token" : "CAAL9MLOLvFIBANMo0FJAYfo08F0mu8I1tnlinlEgCUQ48loQspx97rm0iXnFWZAZB5FeRO5kEhNrbqG2o5Yuat4doXBuuSULsR5JblSGwJf1OQqyMqL7yb5H2nRBgyW77qC7ehy7TBdFpu4qEnstO85CfvFj1LO5UGF2hTfNMZAOtMwiArJy9nToAidnBr7T6oXL1KrftTdlEY5ZAlGT"  
# 		}

# 		graph = get_api(cfg)
# 		print "graph {0}".format(graph)

if __name__ == '__main__':
    unittest.main()