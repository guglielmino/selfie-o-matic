import sys
import os
import json


class ConfigManager(object):

    __config_data = dict()

    def __init__(self, configFilePath):
        self.__config_file = configFilePath
        configDir = os.path.dirname(configFilePath)

        if not os.path.exists(configDir):
            os.makedirs(configDir)

        if os.path.exists(self.__config_file):
            with open(self.__config_file) as data_file:
                self.__config_data = json.load(data_file)

    def getValue(self, config_key):
        res = None

        if config_key in self.__config_data:
            res = self.__config_data[config_key]

        return res

    def setValue(self, config_key, value):
        self.__config_data[config_key] = value
        return self.__saveConfigData()

    def getValues(self):
        return self.__config_data.keys()

    def __saveConfigData(self):
        res = False
        with open(self.__config_file, 'w') as fp:
            json.dump(self.__config_data, fp)
            res = True
