# Fy
## Complex file transfer and ETL using Python and FTP.

## Features
### Workflows
**Workflows** are the heart of Fy. A Fy Workflow is a list of **Transfers** to run. A **Transfer** is defined by a sender and reciever, along with their respective root directory path. Fy will transfer files and folders under the **sender's root directory** to the **reciever's root directory** and can be told to overwrite, skip, append, etc..
TODO: Write a project description
## Installation
TODO: Describe the installation process
## Usage
TODO: Write usage instructions
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
## History
TODO: Write history
## Credits
TODO: Write credits
## License
TODO: Write license

##Code examples (running Fy):
```
from fy.Workflow import Workflow

wf = Workflow()
wf.add_mapping(sender="Server_1", receiver="Server_2", name="Send Server 1 to Server 2")
wf.execute()
```
