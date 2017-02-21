import datetime


def Log(level, message, indent=0):
    """
    Prints the current timestamp, log level, and message to stdout
    :param level: String. The severity of the log. Usually "INFO", "WARN", "ERROR".
    :param message: String. The contents of the log.
    :param indent: Int. How many tabs to indent.
    :return: void
    """
    try:
        print("{:%Y-%m-%d_%H%M%S}".format(datetime.datetime.now()) + "\t" + str(level) + "\t" + ("\t" * indent) + str(
            message))
    except Exception as e:
        LogError(e)
        exit()


def LogError(e):
    try:
        print("{:%Y-%m-%d_%H%M%S}".format(datetime.datetime.now()) + "\t" + "ERROR" + "\t" + str(e))
    except Exception as e:
        print(str(e))
        exit()
