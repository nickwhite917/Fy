import ftplib
import logging

logger = logging.getLogger(__name__)

class Server(object):
    """
    Represents a simple FTP server.
    """

    def __init__(self, server_name, user, password, root_folder=None):
        """
        Initializes the server connection, logs in, and changes to root_folder if one is specified.
        :param server_name:
        :param user:
        :param password:
        :param root_folder:
        """
        try:
            self.name, self.user, self.password = server_name, user, password
            self.ftp_conn = ftplib.FTP(self.name)
            self.ftp_conn.login(self.user, self.password)

            if root_folder is not None:
                self.root_folder = root_folder
                self.ftp_conn.cwd(root_folder)
            else:
                self.root_folder = self.ftp_conn.pwd()
            logger.info("Server initialized: {}. Root: {}.".format(self.name, self.root_folder))
        except Exception as e:
            logger.info("Server initialization failed! Server: {}. Root: {}. Error: {}".format(server_name, root_folder,
                                                                                               str(e)))
            exit()

    def __str__(self):
        return self.name

    def refresh_ftp_conn(self):
        try:
            self.ftp_conn.close()
            self.ftp_conn = ftplib.FTP(self.name)
            self.ftp_conn.login(self.user, self.password)
        except Exception as e:
            logger.error(e)
            exit()

    def mod_folder(self, folder_name, base_path, delete=False):
        exit()
        self.ftp_conn.cwd(base_path)
        sub_folders = self.ftp_conn.nlst()
        for folder in sub_folders:
            try:
                self.ftp_conn.cwd(folder)
                if delete:
                    self.ftp_conn.rmd(folder_name)
                else:
                    self.ftp_conn.mkd(folder_name)
                    self.ftp_conn.cwd("..")
                print(str(e))
            except Exception as e:
                pass
