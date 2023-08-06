from abc import ABCMeta, abstractmethod
from datetime import datetime
import json


class BaseFormatter(metaclass=ABCMeta):
    @abstractmethod
    def format(self):
        pass

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

    @classmethod
    def interpret_keywords(cls, record, fmt):
        change_dict = {"%(asctime)s": str(cls.format_timestamp(record.created)),
                       "%(created)f": str(record.created),
                       "%(filename)s": record.msg['sys']['%(filename)s'],
                       "%(funcName)s": record.msg['sys']['%(funcName)s'],
                       "%(levelname)s": record.levelname,
                       "%(levelno)s": str(record.levelno),
                       "%(lineno)d": str(record.msg['sys']['%(lineno)d']),
                       "%(module)s": record.msg['sys']['%(module)s'],
                       "%(msecs)d": str(record.msecs),
                       "%(name)s": record.name,
                       "%(pathname)s": record.msg['sys']['%(pathname)s'],
                       "%(process)d": str(record.process),
                       "%(processName)s": record.processName,
                       "%(thread)d": str(record.thread),
                       "%(threadName)s": record.threadName}
        for k, v in change_dict.items():
            fmt = fmt.replace(k, v)
        return fmt

    @classmethod
    def serialize(cls, message):
        return bytes(json.dumps(message, default=str), 'utf-8')
