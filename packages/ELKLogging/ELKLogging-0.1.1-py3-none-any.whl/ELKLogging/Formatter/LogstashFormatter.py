from ELKLogging.Formatter.BaseFormatter import BaseFormatter


class LogstashFormatter(BaseFormatter):
    def __init__(self, essential_key_list):
        self.essential_key_list = essential_key_list

    # trace : service name / method / wafer_list / error_log
    # system : cpu(container) / mem(container) / mem(allocate for running method)
    def format(self, record):
        if type(record.msg) == str:
            log_message = record.getMessage()
        elif type(record.msg) == dict:
            if self.check_key_list(list(record.msg.keys())):
                msg = self.make_msg(record)
                log_message = f"[{record.levelname}] >> {msg}"
            else:
                log_message = record.getMessage()
        message = {
            '@timestamp': self.format_timestamp(record.created),
            'message': log_message
        }
        return self.serialize(message)

    def make_msg(self, record):
        msg = ''
        for key in self.essential_key_list:
            new_msg = key + " : " + str(record.msg[key]) + ", "
            msg += new_msg
        msg = msg[:-2]
        return msg

    def check_key_list(self, key_list):
        for key in self.essential_key_list:
            if not key_list.__contains__(key):
                return False
        return True
