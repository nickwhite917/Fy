from fy.Utils import LogError


class Transfer(object):
    """
    Represents a mapping from an existing sender file to a potentially non-existing receiver file.
    """

    def __init__(self, sender_path, sender_file, receiver_path, receiver_file):
        """
        Initializes the Transfer.
        Must be passed a sender path and file, as well as a receiver path and file.
        Paths must be fully qualified.
        :param sender_path: parent path of the file to be transferred
        :param sender_file: name of the file to be transferred, with extension
        :param receiver_path: parent path of the destination file
        :param receiver_file: name of the destination file(can and usually is different from sender_file)
        """
        try:
            self.sender_path, self.sender_file = sender_path, sender_file
            self.receiver_path, self.receiver_file = receiver_path, receiver_file
        except Exception as e:
            LogError(e)
            exit()

    def __str__(self):
        return "sender_path: {}. " \
               "sender_file: {}. " \
               "receiver_path: {}. " \
               "receiver_file: {}.".format(self.sender_path, self.sender_file, self.receiver_path, self.receiver_file)
