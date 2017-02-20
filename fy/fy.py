import sys
import ftplib
import datetime
import os.path


def Log(level, message, indent=0):
    """
    Prints the current timestamp, log level, and message to stdout
    :param level: String. The severity of the log. Usually "INFO", "WARN", "ERROR".
    :param message: String. The contents of the log.
    :param indent: Int. How many tabs to indent.
    :return: void
    """
    print("{:%Y-%m-%d_%H%M%S}".format(datetime.datetime.now()) + "\t" + level + "\t" + ("\t" * indent) + message)


def Shutdown(message="No message supplied."):
    """
    Safely saves state of the program.
    Exits python script safely.
    :return:
    """
    Log("EXIT", "Exiting script with message: {}".format(message))
    exit()


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
            Log("INFO", "Initializing Server: {}. Root: {}.".format(server_name, root_folder))
            self.name, self.user, self.password = server_name, user, password
            self.ftp_conn = ftplib.FTP(self.name)
            self.ftp_conn.login(self.user, self.password)

            if root_folder is not None:
                self.root_folder = root_folder
                self.ftp_conn.cwd(root_folder)
            else:
                self.root_folder = self.ftp_conn.pwd()
            Log("INFO", "Server initialized: {}. Root: {}.".format(self.name, self.root_folder))
        except Exception as e:
            Log("ERROR",
                "Server initialization failed! Server: {}. Root: {}. Error: {}".format(server_name, root_folder,
                                                                                       str(e)))
            Shutdown()

    def __str__(self):
        return self.name

    def refresh_ftp_conn(self):
        self.ftp_conn.close()
        self.ftp_conn = ftplib.FTP(self.name)
        self.ftp_conn.login(self.user, self.password)

    def mod_folder(self, folder_name, base_path, delete=False):
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


class File_Mapping(object):
    """
    Represents a mapping from an existing sender file to a potentially non-existing receiver file.
    """

    def __init__(self, sender_path, sender_file, receiver_path, receiver_file):
        """
        Initializes the File_Mapping.
        Must be passed a sender path and file, as well as a receiver path and file.
        Paths must be fully qualified.
        :param sender_path: parent path of the file to be transferred
        :param sender_file: name of the file to be transferred, with extension
        :param receiver_path: parent path of the destination file
        :param receiver_file: name of the destination file(can and usually is different from sender_file)
        """
        self.sender_path, self.sender_file = sender_path, sender_file
        self.receiver_path, self.receiver_file = receiver_path, receiver_file

    def __str__(self):
        return "sender_path: {}. " \
               "sender_file: {}. " \
               "receiver_path: {}. " \
               "receiver_file: {}.".format(self.sender_path, self.sender_file, self.receiver_path, self.receiver_file)


class Transfer(object):
    def __init__(self, sender=None, receiver=None, log_indent=0, delete_source=False, archive_flag=False):
        Log("INFO", "Initializing Transfer.")
        if sender is None or receiver is None:
            Log("ERROR",
                "Transfer initialization failed! Sender or Receiver not specified. Sender: {}. Receiver: {}.".format(
                    str(sender), str(receiver)), log_indent)
        self.archive_flag, self.delete_source, self.indent, self.receiver, self.sender = archive_flag, delete_source, log_indent, receiver, sender
        Log("INFO", "Transfer initialized. Sender: {}. Receiver: {}.".format(str(self.sender), str(self.receiver)),
            log_indent)

    def build_file_mapping_list(self):
        Log("INFO", "Transfer -> Building file mapping list.", self.indent)
        list = []
        self.sender.ftp_conn.cwd(self.sender.root_folder)
        Log("INFO", "Sender CWD: {}".format(self.sender.root_folder), self.indent + 1)
        self.receiver.ftp_conn.cwd(self.receiver.root_folder)
        Log("INFO", "Receiver CWD: {}".format(self.receiver.root_folder), self.indent + 1)
        for folder in self.sender.ftp_conn.nlst():
            self.sender.ftp_conn.cwd(folder)
            Log("INFO", "Sender PWD: {}".format(self.sender.ftp_conn.pwd()), self.indent + 2)
            for sub_folder in self.sender.ftp_conn.nlst():
                self.sender.ftp_conn.cwd(sub_folder)
                Log("INFO", "Sender PWD: {}".format(self.sender.ftp_conn.pwd()), self.indent + 3)
                listing = self.sender.ftp_conn.nlst()
                if len(listing) > 0:
                    Log("INFO", "Sender nlst: {}".format(str(listing)), self.indent + 3)
                    file = listing[0]
                    sender_path, sender_file = self.sender.ftp_conn.pwd(), file
                    receiver_path = self.receiver.root_folder + "/" + folder + "/"
                    extension = os.path.splitext(file)[1]
                    receiver_file = sub_folder + extension
                    map = File_Mapping(sender_path, sender_file, receiver_path, receiver_file)
                    list.append(map)
                    Log("INFO", "Mapping added to list: {}".format(str(map)), self.indent + 4)
                    Log("INFO", "Mapping List Count: {}".format(len(list)), self.indent + 4)
                self.sender.ftp_conn.cwd("..")
            self.sender.ftp_conn.cwd("..")
        return list

    def send_file(self, mapping):
        self.sender.refresh_ftp_conn()
        self.receiver.refresh_ftp_conn()
        Log("INFO", "Transfer -> Sending file with mapping: {}.".format(str(mapping)), self.indent + 2)

        self.sender.ftp_conn.cwd(mapping.sender_path)
        sender_socket = self.sender.ftp_conn.transfercmd("RETR " + mapping.sender_file)
        try:
            self.receiver.ftp_conn.mkd(mapping.receiver_path)
            Log("INFO", "Created receiver directory: {}".format(mapping.receiver_path), self.indent + 2)
        except:
            pass

        try:
            self.receiver.ftp_conn.cwd(mapping.receiver_path)
            if mapping.receiver_file not in list(self.receiver.ftp_conn.nlst()):
                Log("INFO", "Receiver directory clear for file landing. Beginning transfer.", self.indent + 2)
                if self.archive_flag:
                    archive_dt = "{:%Y-%m-%d%H%M%S}".format(datetime.datetime.now())
                    mapping.receiver_file = str(archive_dt) + mapping.receiver_file
                receiver_socket = self.receiver.ftp_conn.transfercmd("STOR " + mapping.receiver_file)
                state, log_thresh = 0, 0
                while 1:
                    block = sender_socket.recv(1024)
                    if len(block) == 0: break
                    state += len(block)
                    if log_thresh == 100:
                        Log("INFO",
                            "100 file block transferred. Current file size: {} mB".format(str((state / 1024) / 1024)),
                            self.indent + 3)
                        log_thresh = 0
                    else:
                        log_thresh += 1
                    while len(block) > 0:
                        sentlen = receiver_socket.send(block)
                        block = block[sentlen:]
                Log("INFO", "File transfer complete. Sender Bytes Transferred: {}".format(state), self.indent + 2)
                receiver_socket.close()
                sender_socket.close()
                return 0
            else:
                Log("WARN", "File/s present in receiver directory, skipping file transfer.", self.indent + 2)
                sender_socket.close()
                return -1
        except Exception as e:
            Log("ERROR", "File transfer failed! Error: {}".format(str(e)), self.indent + 2)
            return -1

    def run(self):
        Log("INFO", "Beginning transfer run. Sender: {}. Receiver: {}.".format(str(self.sender), str(self.receiver)),
            self.indent)
        file_mapping_list = self.build_file_mapping_list()
        Log("INFO", "File mapping list built. List: {}".format(str('|'.join(str(map) for map in file_mapping_list))),
            self.indent)
        for mapping in file_mapping_list:
            Log("INFO",
                "Beginning file transfer for mapping: {}".format(mapping.sender_path + " to " + mapping.receiver_path),
                self.indent + 1)
            send_file_result = self.send_file(mapping)
            if send_file_result == 0 and self.delete_source:
                # todo self.remove_file(mapping)
                print("remove file here")
            elif send_file_result == 0 and not self.delete_source:
                print("do not remove file here")
            else:
                print("something went wrong in the send file")


class Workflow(object):
    def __init__(self):
        self.transfers = []

    def execute(self):
        if len(self.transfers) > 0:
            for transfer_tuple in self.transfers:
                Log("INFO", "Workflow -> Transfer: {}".format(transfer_tuple[0]))
                transfer_tuple[1].run()

    def add_transfers(self, transfers):
        for transfer in transfers:
            self.transfers.append(transfer)

            # def main():
            #     return 0
            #
            # if __name__ == "__main__":
            #     main()
