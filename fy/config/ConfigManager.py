import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

class ConfigManger(object):
    def __init__(self):
        try:
            self.servers = ConfigParser()
            self.servers.read("fy/config/servers.conf")
            self.options = ConfigParser()
            self.options.read("fy/config/options.conf")
        except Exception as e:
            logger.error(e)
            exit()

    def getServerConfiguration(self, section):
        try:
            section = self.servers[section]
            return [section["Server"], section["User"], section["Password"], section["Init_Dir"]]
        except Exception as e:
            logger.error(e)
            exit()

    def getOptions(self):
        try:
            section = self.options["Options"]
            options = {}
            for option in section.keys():
                for item in section[option].split(','):
                    kv_arr = item.split('=')
                    options[kv_arr[0]] = kv_arr[1]
            return options
        except Exception as e:
            logger.error(e)
            exit()
