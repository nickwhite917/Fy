import os

from fy.Server import Server
from fy.Transfer import Transfer
from fy.Utils import *


class Mapping(object):
    def __init__(self, sender_server=None, receiver_server=None, log_indent=0, delete_source=False, archive_flag=False,
                 name="Un-named Mapping"):
        try:
            if sender_server is None or receiver_server is None:
                Log("ERROR",
                    "Mapping initialization failed! Sender or Receiver not specified. Sender: {}. Receiver: {}.".format(
                        str(sender_server), str(receiver_server)), log_indent)
                raise
            self.archive_flag, self.delete_source, self.indent, self.receiver_server, self.sender_server, self.name = archive_flag, delete_source, log_indent, receiver_server, sender_server, name
            Log("INFO", "Mapping initialized. Sender: {}{}. Receiver: {}{}.".format(str(self.sender_server[0]),
                                                                                    str(self.sender_server[3]),
                                                                                    str(self.receiver_server[0]),
                                                                                    str(self.receiver_server[3])),
                log_indent)
        except Exception as e:
            LogError(e)
            exit()

    def build_file_transfer_list(self):
        try:
            Log("INFO", "Mapping -> Building file transfer list.", self.indent)
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
                        transfer = Transfer(sender_path, sender_file, receiver_path, receiver_file)
                        list.append(transfer)
                        Log("INFO", "Transfer added to list: {}".format(str(transfer)), self.indent + 4)
                        Log("INFO", "Transfer List Count: {}".format(len(list)), self.indent + 4)
                    self.sender.ftp_conn.cwd("..")
                self.sender.ftp_conn.cwd("..")
            return list
        except Exception as e:
            LogError(e)
            exit()

    def send_file(self, transfer):
        try:
            self.sender.refresh_ftp_conn()
            self.receiver.refresh_ftp_conn()
            Log("INFO", "Mapping -> Sending file with config: {}.".format(str(transfer)), self.indent + 2)

            self.sender.ftp_conn.cwd(transfer.sender_path)
            sender_socket = self.sender.ftp_conn.transfercmd("RETR " + transfer.sender_file)
            try:
                self.receiver.ftp_conn.mkd(transfer.receiver_path)
                Log("INFO", "Created receiver directory: {}".format(transfer.receiver_path), self.indent + 2)
            except:
                pass

            try:
                self.receiver.ftp_conn.cwd(transfer.receiver_path)
                if transfer.receiver_file not in list(self.receiver.ftp_conn.nlst()):
                    Log("INFO", "Receiver directory clear for file landing. Beginning transfer.", self.indent + 2)
                    if self.archive_flag:
                        archive_dt = "{:%Y-%m-%d%H%M%S}".format(datetime.datetime.now())
                        transfer.receiver_file = str(archive_dt) + transfer.receiver_file
                    receiver_socket = self.receiver.ftp_conn.transfercmd("STOR " + transfer.receiver_file)
                    state, log_thresh = 0, 0
                    while 1:
                        block = sender_socket.recv(1024)
                        if len(block) == 0: break
                        state += len(block)
                        if log_thresh == 10000:
                            Log("INFO",
                                "10,000 file block transferred. Current file size: {} mB".format(
                                    str((state / 1024) / 1024)),
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
        except Exception as e:
            LogError(e)
            exit()

    def run(self):
        try:
            self.sender = Server(*self.sender_server)
            self.receiver = Server(*self.receiver_server)
            file_transfer_list = self.build_file_transfer_list()
            Log("INFO",
                "File transfer list built. List: {}".format(str('|'.join(str(map) for map in file_transfer_list))),
                self.indent)
            for mapping in file_transfer_list:
                Log("INFO",
                    "Beginning file transfer for item: {}".format(mapping.sender_path + " to " + mapping.receiver_path),
                    self.indent + 1)
                send_file_result = self.send_file(mapping)
                if send_file_result == 0 and self.delete_source:
                    # todo self.remove_file(mapping)
                    print("remove file here")
                elif send_file_result == 0 and not self.delete_source:
                    print("do not remove file here")
                else:
                    Log("WARN",
                        "Send_File had a non-zero return. File was either present or processing failed. See above logs.",
                        self.indent + 1)
            Log("INFO", "Mapping {} finished.".format(self.name))
        except Exception as e:
            LogError(e)
            exit()
