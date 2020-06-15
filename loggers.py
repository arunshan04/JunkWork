# -*- coding: utf-8 -*-
# Description:
# Author: Ilya Mashchenko (ilyam8)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import traceback

from sys import exc_info

try:
    from time import monotonic as time
except ImportError:
    from time import time

#from bases.collection import on_try_except_finally


LOGGING_LEVELS = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}

DEFAULT_LOG_LINE_FORMAT = '%(asctime)s: %(name)s %(levelname)s : %(message)s'
DEFAULT_LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

PYTHON_D_LOG_LINE_FORMAT = '%(asctime)s: %(name)s %(levelname)s: %(module_name)s[%(job_name)s] : %(message)s'
PYTHON_D_LOG_NAME = 'python.d'




def on_try_except_finally(on_except=(None, ), on_finally=(None, )):
    except_func = on_except[0]
    finally_func = on_finally[0]

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                if except_func:
                    except_func(*on_except[1:])
            finally:
                if finally_func:
                    finally_func(*on_finally[1:])
        return wrapper
    return decorator



class BaseLogger(object):
    def __init__(self, logger_name, log_fmt=DEFAULT_LOG_LINE_FORMAT, date_fmt=DEFAULT_LOG_TIME_FORMAT,
                 handler=logging.StreamHandler):
        """
        :param logger_name: <str>
        :param log_fmt: <str>
        :param date_fmt: <str>
        :param handler: <logging handler>
        """
        self.logger = logging.getLogger(logger_name)
        if not self.has_handlers():
            self.severity = 'INFO'
            self.logger.addHandler(handler())
            self.set_formatter(fmt=log_fmt, date_fmt=date_fmt)

    def __repr__(self):
        return '<Logger: {name})>'.format(name=self.logger.name)

    def set_formatter(self, fmt, date_fmt=DEFAULT_LOG_TIME_FORMAT):
        """
        :param fmt: <str>
        :param date_fmt: <str>
        :return:
        """
        if self.has_handlers():
            self.logger.handlers[0].setFormatter(logging.Formatter(fmt=fmt, datefmt=date_fmt))

    def has_handlers(self):
        return self.logger.handlers

    @property
    def severity(self):
        return self.logger.getEffectiveLevel()

    @severity.setter
    def severity(self, level):
        """
        :param level: <str> or <int>
        :return:
        """
        if level in LOGGING_LEVELS:
            self.logger.setLevel(LOGGING_LEVELS[level])

    def debug(self, *msg, **kwargs):
        self.logger.debug(' '.join(map(str, msg)), **kwargs)

    def info(self, *msg, **kwargs):
        self.logger.info(' '.join(map(str, msg)), **kwargs)

    def warning(self, *msg, **kwargs):
        self.logger.warning(' '.join(map(str, msg)), **kwargs)

    def error(self, *msg, **kwargs):
        self.logger.error(' '.join(map(str, msg)), **kwargs)

    def alert(self, *msg,  **kwargs):
        self.logger.critical(' '.join(map(str, msg)), **kwargs)

    @on_try_except_finally(on_finally=(exit, 1))
    def fatal(self, *msg, **kwargs):
        self.logger.critical(' '.join(map(str, msg)), **kwargs)


