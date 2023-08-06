import json
from ELKLogging.Formatter.BaseFormatter import BaseFormatter


class StreamFormatter(BaseFormatter):
    def __init__(self, fmt):
        self.fmt = fmt

    def format(self, record):
        if type(record.msg) == str:
            log_message = record.getMessage()
        elif type(record.msg) == dict:
            if 'detail_message' in list(record.msg.keys()):
                log_message = record.msg['detail_message']
                if type(log_message) == dict:
                    log_message = json.dumps(log_message)
            else:
                log_message = record.getMessage()
        message = self.interpret_keywords(record, self.fmt)
        message = message.replace("%(message)s", log_message)

        return message
