
import unittest

from services.client.ws_client import WsClient
from config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):

	def test_read_setting(self):
		sett = ConfigManager()
		
		res = sett.getValue("FB_ALBUM_ID")
		self.assertTrue(res)

	def test_write_setting(self):
		sett = ConfigManager()
		res = sett.setValue("FB_ALBUM_ID", "123")
		self.assertEqual(sett.getValue("FB_ALBUM_ID"), "123")


# class TestWsClient(unittest.TestCase):
# 	def test_ws_client(self):
# 		client = WsClient()
# 		client.register_myself("123")
# 		self.assertTrue(True)


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