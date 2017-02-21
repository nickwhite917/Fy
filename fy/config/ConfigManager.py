from configparser import ConfigParser

from fy.Utils import LogError


class ConfigManger(object):
    def __init__(self):
        try:
            self.servers = ConfigParser()
            self.servers.read("fy/config/servers.conf")
            self.options = ConfigParser()
            self.options.read("fy/config/options.conf")
        except Exception as e:
            LogError(e)
            exit()

    def getServerConfiguration(self, section):
        try:
            section = self.servers[section]
            return [section["Server"], section["User"], section["Password"], section["Init_Dir"]]
        except Exception as e:
            LogError(e)
            exit()

    def getOptions(self, section):
        try:
            section = self.options[section]
            exit()
        except Exception as e:
            LogError(e)
            exit()
