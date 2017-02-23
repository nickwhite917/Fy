import datetime
import logging
import os

from fy.Server import Server
from fy.Transfer import Transfer

logger = logging.getLogger(__name__)

class Mapping(object):
    def __init__(self, sender_server=None, receiver_server=None, delete_source=False, archive_flag=False,
                 name="Un-named Mapping", options=None):
        try:
            if sender_server is None or receiver_server is None:
                logger.error(
                    "Mapping initialization failed! Sender or Receiver not specified. Sender: {}. Receiver: {}.".format(
                        str(sender_server), str(receiver_server)))
                raise
            self.archive_flag, self.delete_source, self.receiver_server, self.sender_server, self.name, self.options = \
                archive_flag, delete_source, receiver_server, sender_server, name, options
            logger.info("Mapping initialized. Sender: {}{}. Receiver: {}{}."
                        .format(str(self.sender_server[0]),
                                str(self.sender_server[3]),
                                str(self.receiver_server[0]),
                                str(self.receiver_server[3])))
        except Exception as e:
            logger.error(e)
            exit()

    def build_file_transfer_list(self):
        try:
            logger.info("Mapping -> Building file transfer list.")
            list = []
            self.sender.ftp_conn.cwd(self.sender.root_folder)
            logger.info("Sender CWD: {}".format(self.sender.root_folder))
            self.receiver.ftp_conn.cwd(self.receiver.root_folder)
            logger.info("Receiver CWD: {}".format(self.receiver.root_folder))
            for folder in self.sender.ftp_conn.nlst():
                self.sender.ftp_conn.cwd(folder)
                logger.info("Sender PWD: {}".format(self.sender.ftp_conn.pwd()))
                for sub_folder in self.sender.ftp_conn.nlst():
                    self.sender.ftp_conn.cwd(sub_folder)
                    logger.info("Sender PWD: {}".format(self.sender.ftp_conn.pwd()))
                    listing = self.sender.ftp_conn.nlst()
                    if len(listing) > 0:
                        logger.info("Sender nlst: {}".format(str(listing)))
                        file = listing[0]
                        sender_path, sender_file = self.sender.ftp_conn.pwd(), file
                        receiver_path = self.receiver.root_folder + "/" + folder + "/"
                        extension = os.path.splitext(file)[1]
                        receiver_file = None
                        if self.options is not None:
                            try:
                                receiver_file = self.options[sub_folder]
                            except:
                                try:
                                    receiver_file = self.options[file]
                                except:
                                    pass
                        transfer = Transfer(sender_path, sender_file, receiver_path, receiver_file)
                        list.append(transfer)
                        logger.info("Transfer added to list: {}".format(str(transfer)))
                        logger.info("Transfer List Count: {}".format(len(list)))
                    self.sender.ftp_conn.cwd("..")
                self.sender.ftp_conn.cwd("..")
            return list
        except Exception as e:
            logger.error(e)
            exit()

    def send_file(self, transfer):
        try:
            self.sender.refresh_ftp_conn()
            self.receiver.refresh_ftp_conn()
            logger.info("Mapping -> Sending file with config: {}.".format(str(transfer)))

            self.sender.ftp_conn.cwd(transfer.sender_path)
            sender_socket = self.sender.ftp_conn.transfercmd("RETR " + transfer.sender_file)
            try:
                self.receiver.ftp_conn.mkd(transfer.receiver_path)
                logger.info("Created receiver directory: {}".format(transfer.receiver_path))
            except:
                pass

            try:
                self.receiver.ftp_conn.cwd(transfer.receiver_path)
                if transfer.receiver_file not in list(self.receiver.ftp_conn.nlst()):
                    logger.info("Receiver directory clear for file landing. Beginning transfer.")
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
                            logger.info("10,000 file block transferred. Current file size: {} mB".format(
                                str((state / 1024) / 1024)))
                            log_thresh = 0
                        else:
                            log_thresh += 1
                        while len(block) > 0:
                            sentlen = receiver_socket.send(block)
                            block = block[sentlen:]
                            logger.info("File transfer complete. Sender Bytes Transferred: {}".format(state))
                    receiver_socket.close()
                    sender_socket.close()
                    return 0
                else:
                    logger.warning("File/s present in receiver directory, skipping file transfer.")
                    sender_socket.close()
                    return -1
            except Exception as e:
                logger.error("File transfer failed! Error: {}".format(str(e)))
                return -1
        except Exception as e:
            logger.error(e)
            exit()

    def run(self):
        try:
            self.sender = Server(*self.sender_server[0:4])
            self.receiver = Server(*self.receiver_server[0:4])
            file_transfer_list = self.build_file_transfer_list()
            logger.info(
                "File transfer list built. List: {}".format(str('|'.join(str(map) for map in file_transfer_list))))
            for mapping in file_transfer_list:
                logger.info(
                    "Beginning file transfer for item: {}".format(mapping.sender_path + " to " + mapping.receiver_path))
                send_file_result = self.send_file(mapping)
                if send_file_result == 0 and self.delete_source:
                    # todo self.remove_file(mapping)
                    print("remove file here")
                elif send_file_result == 0 and not self.delete_source:
                    print("do not remove file here")
                else:
                    logger.warning(
                        "Send_File had a non-zero return. File was either present or processing failed. See above logs.")
            logger.info("Mapping {} finished.".format(self.name))
        except Exception as e:
            logger.error(e)
            exit()
