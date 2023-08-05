import os
from logging.handlers import RotatingFileHandler
from ELKLogging.Formatter.FileFormatter import FileFormatter


class FileStreamHandler(RotatingFileHandler, object):
    def __init__(self, folder_path, file_name, encoding='UTF-8', maxBytes=20 * 1024 * 1024, backupCount=14,
                 fmt="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s"):
        self.makeDirectory(folder_path=folder_path)
        file_path = os.path.join(folder_path, file_name)
        super(FileStreamHandler, self).__init__(filename=file_path, encoding=encoding, maxBytes=maxBytes,
                                                backupCount=backupCount)
        self.formatter = FileFormatter(fmt)

    def makeDirectory(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'

