from enum import Enum
from ELKLogging.Handler.StreamHandler import ConsoleStreamHandler
from ELKLogging.Handler.FileHandler import FileStreamHandler
from ELKLogging.Handler.LogstashHandler import LogstashHandler


def enum(**named_value):
    return type('Enum', (), named_value)


LOG_LEVEL = enum(DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50)


class MemLevel(Enum):
    KB = 1
    MB = 2
    GB = 3


class HANDLER(Enum):
    LOGSTASH = LogstashHandler
    STREAM = ConsoleStreamHandler
    FILE = FileStreamHandler
