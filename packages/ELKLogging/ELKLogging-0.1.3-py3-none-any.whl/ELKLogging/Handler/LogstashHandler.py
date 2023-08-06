from ELKLogging.Formatter.LogstashFormatter import LogstashFormatter
from logging.handlers import SocketHandler


class LogstashHandler(SocketHandler, object):
    def __init__(self, essential_key_list, host, port):
        super(LogstashHandler, self).__init__(host, port)
        self.formatter = LogstashFormatter(essential_key_list)
        self.essential_key_list = essential_key_list

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'
