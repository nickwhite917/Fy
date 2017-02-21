# Fy
Pronounced (/'faɪ/)

Transfer files recursively from one server to another using Python and FTP. 

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
import fy.fy

ftp_servers = {
        "My_Ftp_Site_Source": ["ftp.yoursite.com", "usrname1", "paswd1", "/home/myuser/data"]
        ,"My_Ftp_Site_Dest_1": ["ftp2.yoursite.com", "us3r2name1", "12paswd1", "/home/myuser/data1"]
        ,"My_Ftp_Site_Dest_2": ["ftp3.yoursite.com", "us3r2name1", "12paswd1", "/home/myuser/data1"]
    }

source_site = fy.Server(*ftp_servers["My_Ftp_Site_Source"])
dest_1 = fy.Server(*ftp_servers["My_Ftp_Site_Dest_1"])

source_to_dest_1 = fy.Transfer(source_site, dest_1)

# dest_2 = Server(*ftp_servers["My_Ftp_Site_Dest_2"])
# source_to_dest_2 = Transfer(source_site, dest_2, archive_flag=True)

wf = fy.Workflow()
wf.add_transfers([("Workflow name here. ", source_to_dest_1)])

wf.execute()
```
