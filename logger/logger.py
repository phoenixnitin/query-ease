import os
import logging

from logging.handlers import TimedRotatingFileHandler


class Logger:
    __logger = None

    @classmethod
    def __initialize_logger(cls):
        cls.__logger = logging.getLogger('app.log')
        formatter = logging.Formatter('[%(asctime)s] [%(process)-5s] [%(threadName)-10s] [%(levelname)-5s] %(message)s')
        os.makedirs('./logs', exist_ok=True)
        handler = TimedRotatingFileHandler(filename='logs/app.log', when='midnight', interval=1, backupCount=30)
        handler.setFormatter(formatter)
        cls.__logger.addHandler(handler)
        cls.__logger.setLevel(logging.INFO)

    @classmethod
    def get_logger(cls):
        if cls.__logger:
            return cls.__logger
        cls.__initialize_logger()
        return cls.__logger
