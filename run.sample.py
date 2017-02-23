import logging

from fy.Workflow import Workflow

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='fy.log',
                    level=logging.DEBUG)

wf = Workflow()
wf.add_mapping(sender="Server_1", receiver="Server_2", name="Send Server 1 to Server 2")
wf.execute()
