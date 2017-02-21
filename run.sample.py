from fy.Workflow import Workflow

wf = Workflow()
wf.add_mapping(sender="Server_1", receiver="Server_2", name="Send Server 1 to Server 2")
wf.execute()
