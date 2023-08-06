import logging
import io
import sys

class LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg):
        if msg.endswith('\n'):
            self.buf.append(msg.strip('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self):
        pass

class CachedLogger(object):
    def __init__(self):
        self.__log_capture_string = None
    def start_logging(self):
        self.__old_stdout = sys.stdout
        self.__log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.__log_capture_string)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        self.__logger = logging.getLogger('basic_logger')
        sys.stdout = LoggerWriter(self.__logger.info)
        self.__logger .setLevel(logging.DEBUG)
        self.__logger .addHandler(ch)
        return self.__logger

    def stop_logging(self):
        log_contents = self.__log_capture_string.getvalue()
        self.__log_capture_string.flush()
        sys.stdout = self.__old_stdout
        print(log_contents)
        return log_contents

    def __del__(self):
        if self.__log_capture_string:
            self.__log_capture_string.close()
