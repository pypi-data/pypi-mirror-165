from ELKLogging.Formatter.StreamFormatter import StreamFormatter
from logging import StreamHandler


class ConsoleStreamHandler(StreamHandler, object):
    def __init__(self, fmt="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s"):
        super(ConsoleStreamHandler, self).__init__()
        self.formatter = StreamFormatter(fmt)

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'