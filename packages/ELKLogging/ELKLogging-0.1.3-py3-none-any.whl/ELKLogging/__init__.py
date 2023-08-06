import logging
import os
import re
import sys
import time
import traceback
import inspect
import functools
from functools import wraps
from ELKLogging.Handler.FileHandler import FileStreamHandler
from ELKLogging.Handler.LogstashHandler import LogstashHandler
from ELKLogging.Handler.StreamHandler import ConsoleStreamHandler
from ELKLogging.Infra.Singletone import Singletone
from ELKLogging.Infra.SystemMetricsCatcher import SystemMetricsCatcher
from ELKLogging.Infra.Enum import *


class Logger(metaclass=Singletone):
    def __init__(self, logger_name='ELK_LOGGER', log_level=LOG_LEVEL.INFO, config=None):
        self.end_time = dict()
        self.start_time = dict()
        if type(config) == dict:
            self.initialize_logger(config)
        else:
            self.__logger = logging.getLogger(logger_name)
            self.__logger.setLevel(log_level)
            self.__message_data = {}
            self.flush_message_data()
            self.set_message_data('service_name', logger_name)

    @classmethod
    def str_to_class(cls, class_name):
        return getattr(sys.modules[__name__], class_name)

    @classmethod
    def traceback_error(cls):
        return traceback.format_exc()

    @classmethod
    def function_name(cls, frame, funcName):
        if funcName in ['get', 'post'] and 'self' in frame.f_locals and hasattr(frame.f_locals['self'], 'endpoint'):
            return frame.f_locals['self'].endpoint
        elif funcName in ['run'] and 'args' in frame.f_locals and len(frame.f_locals['args']) and type(
                frame.f_locals['args'][0]) == functools.partial:
            tempFuncName = str(frame.f_locals['args'][0].func)
            tempFuncName = tempFuncName[tempFuncName.find('<function ') + 10:tempFuncName.find(' at 0x')]
            return tempFuncName
        return funcName

    def initialize_logger(self, config_data):
        self.__logger = logging.getLogger(config_data['root']['logger_name'])
        self.__logger.setLevel(config_data['root']['level'])
        handler_list = config_data['root']['handlers']
        for handler in handler_list:
            handler_class = self.str_to_class(config_data['handlers'][handler]['class'])
            log_level = config_data['handlers'][handler].get('level')
            if handler_class == LogstashHandler:
                host = config_data['handlers'][handler].get('ip')
                port = int(config_data['handlers'][handler].get('port'))
                essential_key_list = config_data['handlers'][handler].get('column_list')
                tmp_handler = LogstashHandler(essential_key_list=essential_key_list, host=host, port=port)
            elif handler_class == FileStreamHandler:
                fmt = config_data['handlers'][handler].get('formatter')
                if fmt in config_data['formatters']:
                    fmt = config_data['formatters'][fmt]['format']
                folder_path = config_data['handlers'][handler].get('folderpath')
                file_name = config_data['handlers'][handler].get('filename')
                encoding = config_data['handlers'][handler].get('encoding', 'UTF-8')
                maxBytes = config_data['handlers'][handler].get('maxBytes', '20MB')
                backupCount = config_data['handlers'][handler].get('backupCount', 14)
                level = [n.value for n in MemLevel if n.name in maxBytes]
                if len(level) == 1:
                    level = level[0]
                else:
                    level = 2
                numbers = int(re.sub(r'[^0-9]', '', maxBytes))
                maxBytes = numbers * pow(1024, level)
                tmp_handler = FileStreamHandler(folder_path=folder_path, file_name=file_name, fmt=fmt,
                                                encoding=encoding, maxBytes=maxBytes, backupCount=backupCount)
            elif handler_class == ConsoleStreamHandler:
                fmt = config_data['handlers'][handler].get('formatter')
                if fmt in config_data['formatters']:
                    fmt = config_data['formatters'][fmt]['format']
                tmp_handler = ConsoleStreamHandler(fmt=fmt)
            else:
                pass
            tmp_handler.setLevel(log_level)
            self.__logger.addHandler(tmp_handler)
        self.__message_data = {}
        self.flush_message_data()
        self.set_message_data('service_name', config_data['root']['logger_name'])

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger_name):
        self.__logger = logging.getLogger(logger_name)

    @property
    def message_data(self):
        return self.__message_data

    @message_data.setter
    def message_data(self, message):
        self.__message_data = message

    def set_message_data(self, key, value):
        self.__message_data[key] = value
        return self.__message_data

    def flush_message_data(self):
        for handler in self.logger.handlers:
            if type(handler) == HANDLER.LOGSTASH.value:
                for key in handler.essential_key_list:
                    self.set_message_data(key, '0')

    def add_handler(self, handler):
        self.logger.addHandler(handler)

    def remove_handler(self, handler_list):
        tmp_handler = []
        cnt = 0
        for idx in range(len(self.logger.handlers)):
            idx -= cnt
            if type(self.logger.handlers[idx]) not in handler_list:
                tmp_handler.append(self.logger.handlers[idx])
                self.logger.removeHandler(self.logger.handlers[idx])
                cnt += 1
        return tmp_handler

    def restore_handler(self, handler_list):
        for hand in handler_list:
            self.logger.addHandler(hand)

    def findCaller(self):
        f = sys._getframe()
        if f is not None:
            f = f.f_back.f_back
        while hasattr(f, "f_code"):
            co = f.f_code
            if co.co_name == 'wrapper':
                f = f.f_back
                continue
            if co.co_name == 'light':
                funcName = f.f_locals['self'].id
            else:
                funcName = co.co_name
            self.message_data['sys'] = dict()
            frame = f
            funcName = self.function_name(frame=frame, funcName=funcName)
            self.set_message_data(key='method', value=funcName)
            self.message_data['sys']['%(funcName)s'] = funcName
            self.message_data['sys']['%(lineno)d'] = f.f_lineno
            self.message_data['sys']['%(pathname)s'] = co.co_filename
            self.message_data['sys']['%(module)s'] = os.path.splitext(co.co_filename)[0]
            self.message_data['sys']['%(filename)s'] = os.path.basename(co.co_filename)
            break

    def info(self, message=' ', destination=[HANDLER.LOGSTASH, HANDLER.FILE, HANDLER.STREAM]):
        remove_handler = self.remove_handler([n.value for n in destination])
        self.message_data['detail_message'] = message
        self.findCaller()
        self.logger.info(self.message_data)
        self.restore_handler(remove_handler)

    def error(self, message=' ', destination=[HANDLER.LOGSTASH, HANDLER.FILE, HANDLER.STREAM]):
        remove_handler = self.remove_handler([n.value for n in destination])
        self.message_data['detail_message'] = message
        self.findCaller()
        self.logger.error(self.message_data)
        self.restore_handler(remove_handler)

    def warning(self, message=' ', destination=[HANDLER.LOGSTASH, HANDLER.FILE, HANDLER.STREAM]):
        remove_handler = self.remove_handler([n.value for n in destination])
        self.message_data['detail_message'] = message
        self.findCaller()
        self.logger.warning(self.message_data)
        self.restore_handler(remove_handler)

    def debug(self, message=' ', destination=[HANDLER.LOGSTASH, HANDLER.FILE, HANDLER.STREAM]):
        remove_handler = self.remove_handler([n.value for n in destination])
        self.message_data['detail_message'] = message
        self.findCaller()
        self.logger.debug(self.message_data)
        self.restore_handler(remove_handler)

    def critical(self, message=' ', destination=[HANDLER.LOGSTASH, HANDLER.FILE, HANDLER.STREAM]):
        remove_handler = self.remove_handler([n.value for n in destination])
        self.message_data['detail_message'] = message
        self.findCaller()
        self.logger.critical(self.message_data)
        self.restore_handler(remove_handler)


    def systemlog_tracing_start(self):
        frame = inspect.currentframe().f_back
        funcName = frame.f_code.co_name
        funcName = self.function_name(frame=frame, funcName=funcName)
        self.start_time[funcName] = time.time()
        SystemMetricsCatcher.tracing_start()

    def systemlog_tracing_end(self):
        frame = inspect.currentframe().f_back
        funcName = frame.f_code.co_name
        funcName = self.function_name(frame=frame, funcName=funcName)
        self.end_time[funcName] = time.time()
        cpu_usage, mem_usage = SystemMetricsCatcher.cpu_usage_percent(), SystemMetricsCatcher.tracing_mem()
        running_time = round(self.end_time[funcName] - self.start_time[funcName],3)
        self.set_message_data(key='method', value=funcName)
        self.set_message_data(key='cpu_usage', value=cpu_usage)
        self.set_message_data(key='mem_usage', value=mem_usage)
        self.set_message_data(key='running_time', value=running_time)
        self.findCaller()

    # decorator
    def wafer_logstash(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                isresult = False
                start_time = time.time()
                SystemMetricsCatcher.tracing_start()
                result = func(*args, **kwargs)
                cpu_usage, mem_usage = SystemMetricsCatcher.cpu_usage_percent(), SystemMetricsCatcher.tracing_mem()
                end_time = time.time()
                frame = sys._getframe()
                funcName = func.__name__
                funcName = self.function_name(frame=frame, funcName=funcName)
                self.set_message_data(key='method', value=funcName)
                self.set_message_data(key='cpu_usage', value=cpu_usage)
                self.set_message_data(key='mem_usage', value=mem_usage)
                self.set_message_data(key='running_time', value=round(end_time - start_time,3))
                if result and (type(result) == str and result.startswith("Traceback")) or (hasattr(result, 'status_code') and result.status_code != 200):
                    isresult = True
                    raise
                self.info(destination=[HANDLER.LOGSTASH])
                return result
            except Exception:
                if isresult:
                    self.error(message=result, destination=[HANDLER.LOGSTASH])
                else:
                    self.error(destination=[HANDLER.LOGSTASH])
                return result
        return wrapper