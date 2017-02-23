import logging

from fy.Mapping import Mapping
from fy.config.ConfigManager import ConfigManger

logger = logging.getLogger(__name__)

class Workflow(object):
    def __init__(self, name="Un-named Workflow"):
        try:
            self.mappings = []
            self.config = ConfigManger()
            self.name = name
            logger.info("Workflow: {} has been initialized.".format(self.name))
        except Exception as e:
            logger.error(e)
            exit()

    def execute(self):
        try:
            if len(self.mappings) > 0:
                for mapping_tuple in self.mappings:
                    logger.info("Workflow -> Mapping: {}".format(mapping_tuple.name))
                    mapping_tuple.run()
                    logger.info("Workflow {} finished.".format(self.name))
        except Exception as e:
            logger.error(e)
            exit()

    def add_mapping(self, sender, receiver, name=None):
        try:
            sender_server = self.config.getServerConfiguration(sender)
            receiver_server = self.config.getServerConfiguration(receiver)
            options = self.config.getOptions()

            mapping = Mapping(sender_server=sender_server, receiver_server=receiver_server, name=name, options=options)
            self.mappings.append(mapping)
        except Exception as e:
            logger.error(e)
            exit()
