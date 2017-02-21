from configparser import ConfigParser

from fy.Utils import LogError


class ConfigManger(object):
    def __init__(self):
        try:
            self.config = ConfigParser()
            self.config.read("fy/fy.conf")
        except Exception as e:
            LogError(e)
            exit()

    def getServerConfiguration(self, section):
        try:
            section = self.config[section]
            return [section["Server"], section["User"], section["Password"], section["Init_Dir"]]
        except Exception as e:
            LogError(e)
            exit()
