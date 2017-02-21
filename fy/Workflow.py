from fy.Mapping import Mapping
from fy.Utils import *
from fy.config.ConfigManager import ConfigManger


class Workflow(object):
    def __init__(self, name="Un-named Workflow"):
        try:
            self.mappings = []
            self.config = ConfigManger()
            self.name = name
            Log("INFO", "Workflow: {} has been initialized.".format(self.name))
        except Exception as e:
            LogError(e)
            exit()

    def execute(self):
        try:
            if len(self.mappings) > 0:
                for mapping_tuple in self.mappings:
                    Log("INFO", "Workflow -> Mapping: {}".format(mapping_tuple.name))
                    mapping_tuple.run()
                Log("INFO", "Workflow {} finished.".format(self.name))
        except Exception as e:
            LogError(e)
            exit()

    def add_mapping(self, sender, receiver, name=None):
        try:
            sender_server = self.config.getServerConfiguration(sender)
            receiver_server = self.config.getServerConfiguration(receiver)

            mapping = Mapping(sender_server=sender_server, receiver_server=receiver_server, name=name)
            self.mappings.append(mapping)
        except Exception as e:
            LogError(e)
            exit()
