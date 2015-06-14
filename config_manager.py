import sys

try:
	import settings
except:
	print "ERROR -- You need `settings.py` with application settings (create if if doesn't exists)"
	raise

FB_APP_ID="841335565958226"

class ConfigManager(object):

	def getValue(self, config_key):
		mod_dic = self.__getModuleDict()
		res = None

		if mod_dic and config_key in mod_dic:
			res = mod_dic[config_key]

		return res

	def setValue(self, config_key, value):
		res = False

		mod_dic = self.__getModuleDict()
		if mod_dic:
			mod_dic[config_key] = value
			res = True

		return res




	def __getModuleDict(self):
		#module = sys.modules[self.__module__]
		module = sys.modules['settings']
		return module.__dict__
