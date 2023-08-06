class DeprecatedLogger(object):
    def __init__(self):
        print(
            "Deprecated logger, please use 'from puts import get_logger; logger = get_logger();' instead"
        )

    def debug(self, msg):
        print(msg)

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

    def critical(self, msg):
        print(msg)

    def exception(self, msg):
        print(msg)


logger = DeprecatedLogger()
