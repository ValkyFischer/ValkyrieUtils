#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module provides a flexible logging utility for creating log messages
    with various log levels, including info, debug, warning, error, and critical.
    The log messages can be directed to a log file and/or the console.
    Additionally, it supports formatting log messages with caller information
    and customizable message components.
--------

Example:
    >>> log = ValkyrieLogger('info', '.\\log\\logger.log', 'ValkyrieLogger', True)
    >>> log.info(1, 1, 'val1,%s,val2,%s' % (10, 20))
    2021-10-01 00:00:00,000 | INFO    | ValkyrieLogger | ValkyrieLogger.py | 1 | 1 | val1,10,val2,20
    >>> log.info(1, 2, 'val1', 10, 'val2', 20)
    2021-10-01 00:00:00,000 | INFO    | ValkyrieLogger | ValkyrieLogger.py | 1 | 2 | val1 | 10 | val2 | 20
    >>> log.error('# This is a test message')
    2021-10-01 00:00:00,000 | ERROR   | ValkyrieLogger | ValkyrieLogger.py | # This is a test message :: Traceback (most recent call last):
        File "ValkyrieLogger.py", line 123, in <module>
            log.Error('# This is a test message')
        File "ValkyrieLogger.py", line 100, in Error
            traceMsg = traceback.format_exc()
    TypeError: format_exc() missing 1 required positional argument: 'limit'
    
"""

import logging.handlers
import inspect
import traceback
import sys


# ===============================


LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


# ===============================


class ValkyrieLogger:
    """
    Initialize a log instance.

    Args:
        level (str): The log level for this log object (e.g., 'debug', 'info', 'warning').
        filePath (str, optional): The absolute path to the log file. Default is None.
        appName (str, optional): The name of the application. Default is 'CruiseLog'.
        useInspect (bool, optional): Whether to use inspect to gather caller information. Default is False.

    """
    def __init__(self, level, filePath = None, appName = 'ValkyrieLogger', useInspect = False, debug = False):
        self.LOG_LEVEL = LOG_LEVELS.get(level, logging.NOTSET)
        self.PATH = filePath
        self.IsConsoleOnly = False
        if self.PATH is None or len(self.PATH) <= 0: self.IsConsoleOnly = True
        self.Logger = self.GetLogger(appName) if not self.IsConsoleOnly else None
        self.ConsoleLogger = self.GetConsoleLogger(appName + '_Console', False)
        self.ConsoleErrLogger = self.GetConsoleLogger(appName + '_ConsoleErr', True)
        self.useInspect = useInspect
        if debug: self.info("Started a new Valkyrie Logger instance")
    
    @staticmethod
    def _ConvertUnicode(param):
        """
        Convert the input parameter to a string representation.

        This method handles the conversion of various types to string.
        If the input is None, an empty string is returned. For other types,
        the input is converted to its string representation.

        Args:
            param (any): The input parameter to be converted to a string.

        Returns:
            str: The string representation of the input parameter.
        """
        if param is None:
            return ''
        elif isinstance(param, str):
            return str(param)
        elif isinstance(param, list):
            return str(param)
        elif isinstance(param, dict):
            return str(param)
        elif isinstance(param, int) or isinstance(param, float):
            return str(param)
        else:
            return str(param)
    
    def GetLogger(self, loggerName):
        """
        Get a logger instance.

        Args:
            loggerName (str): The unique logger name.

        Returns:
            logging.Logger: The logger instance.
        """
        logger = logging.getLogger(loggerName)
        logger.setLevel(self.LOG_LEVEL)
        
        if not logger.handlers:
            handlerFile = logging.handlers.TimedRotatingFileHandler(self.PATH, "H", 1, 0)
            handlerFile.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s%(message)s"))
            logger.addHandler(handlerFile)
        
        return logger
    
    def GetConsoleLogger(self, loggerName, isUseStdErr):
        """
        Get a console logger instance.

        Args:
            loggerName (str): The unique logger name.
            isUseStdErr (bool): Whether to use standard error output.

        Returns:
            logging.Logger: The console logger instance.
        """
        logger = logging.getLogger(loggerName)
        logger.setLevel(self.LOG_LEVEL)
        
        if not logger.handlers:
            consoleLogger = logging.StreamHandler(sys.stderr if isUseStdErr else sys.stdout)
            consoleLogger.setLevel(self.LOG_LEVEL)
            consoleLogger.setFormatter(ColorfulFormatter("%(asctime)s | %(levelname)-7s%(message)s"))
            logger.addHandler(consoleLogger)
        
        return logger
    
    def ProcessMsg(self, msg, kwMsg, addStr = ''):
        """
        Build a log message.

        Args:
            msg (tuple): A tuple of message components.
            kwMsg (dict): A dictionary of key-value message components.
            addStr (str, optional): Additional string to add to the message. Default is ''.

        Returns:
            str: The formatted log message.
        """
        if self.useInspect:
            fullPath, lineNumber, functionName = inspect.getouterframes(inspect.currentframe())[2][1:4]
            fileName = fullPath.split('\\')
            if len(fileName) == 1:
                fileName = fullPath.split('/')[-1]
            else:
                fileName = fileName[-1]
            
            retMsg = u' | %-20s | %-5s | %-20s' % (fileName, lineNumber, functionName)
        else:
            retMsg = u''
        
        if len(msg) == 1 and isinstance(msg[0], str):
            retMsg += ' | ' + msg[0]
        elif isinstance(msg, tuple) or isinstance(msg, list):
            for item in msg:
                retMsg += ' | ' + self._ConvertUnicode(item)
        
        for k, v in kwMsg.items():
            retMsg += ' | ' + str(k) + ' | ' + str(v)
        
        return retMsg + addStr
    
    def info(self, *strMsg, **kwStrMsg):
        """
        Write a log message at the info level.

        Args:
            *strMsg: Variable positional arguments for the log message.
            **kwStrMsg: Variable keyword arguments for the log message.
        """
        if self.LOG_LEVEL > logging.INFO:
            return None
        
        message = self.ProcessMsg(strMsg, kwStrMsg)
        
        if self.IsConsoleOnly:
            self.ConsoleLogger.info(message)
        else:
            self.Logger.info(message)
            if self.PATH is not None:
                self.ConsoleLogger.info(message)
    
    def debug(self, *strMsg, **kwStrMsg):
        """
        Write a log message at the debug level.

        Args:
            *strMsg: Variable positional arguments for the log message.
            **kwStrMsg: Variable keyword arguments for the log message.
        """
        if self.LOG_LEVEL > logging.DEBUG:
            return None
        
        message = self.ProcessMsg(strMsg, kwStrMsg)
        
        if self.IsConsoleOnly:
            self.ConsoleLogger.debug(message)
        else:
            self.Logger.debug(message)
            if self.PATH is not None:
                self.ConsoleLogger.debug(message)
    
    def error(self, *strMsg, **kwStrMsg):
        """
        Write a log message at the error level.

        Args:
            *strMsg: Variable positional arguments for the log message.
            **kwStrMsg: Variable keyword arguments for the log message.
        """
        if self.LOG_LEVEL > logging.ERROR:
            return None
        
        traceMsg = traceback.format_exc()
        if traceMsg is not None and traceMsg != 'None\n':
            message = self.ProcessMsg(strMsg, kwStrMsg, (" :: " + traceMsg))
        else:
            message = self.ProcessMsg(strMsg, kwStrMsg, '')
        
        if self.IsConsoleOnly:
            self.ConsoleErrLogger.error(message)
        else:
            self.Logger.error(message)
            if self.PATH is not None:
                self.ConsoleErrLogger.error(message)
    
    def console(self, level, *strMsg, **kwStrMsg):
        """
        Write a console log message.

        Args:
            level (str): The log level for the console message (e.g., 'info', 'debug').
            *strMsg: Variable positional arguments for the log message.
            **kwStrMsg: Variable keyword arguments for the log message.
        """
        
        logLevel = LOG_LEVELS.get(level, logging.NOTSET)
        if self.LOG_LEVEL > logLevel:
            return None
        
        self.ConsoleLogger.log(logLevel, self.ProcessMsg(strMsg, kwStrMsg))
        if not self.IsConsoleOnly:
            self.Logger.log(logLevel, self.ProcessMsg(strMsg, kwStrMsg))
    
    def consoleError(self, *strMsg, **kwStrMsg):
        """
        Write a console error log message.

        Args:
            *strMsg: Variable positional arguments for the log message.
            **kwStrMsg: Variable keyword arguments for the log message.
        """
        if self.LOG_LEVEL > logging.ERROR:
            return None
        
        self.ConsoleErrLogger.error(self.ProcessMsg(strMsg, kwStrMsg))
        if not self.IsConsoleOnly:
            traceMsg = traceback.format_exc()
            if traceMsg is not None and traceMsg != 'None\n':
                message = self.ProcessMsg(strMsg, kwStrMsg, (" :: " + traceMsg))
            else:
                message = self.ProcessMsg(strMsg, kwStrMsg, '')
            self.Logger.error(message)


class ColorfulFormatter(logging.Formatter):
    # Define color codes for test
    BOX = "\033[0;51m"
    BOX_T = "\033[0;52m"
    
    
    # Define color codes
    GRAY = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    
    # Define color codes for background colors
    BG_GRAY = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Define color codes for bold colors
    GRAY_BOLD = "\033[90m"
    RED_BOLD = "\033[91m"
    GREEN_BOLD = "\033[92m"
    YELLOW_BOLD = "\033[93m"
    BLUE_BOLD = "\033[94m"
    PURPLE_BOLD = "\033[95m"
    CYAN_BOLD = "\033[96m"
    WHITE_BOLD = "\033[97m"
    
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    UNDERLINE_BOLD = "\033[0;21m"
    BLINK = "\033[5m"
    TEST = "\033[6m"
    NEGATIVE = "\033[7m"
    INVISIBLE = "\033[8m"
    CROSSED = "\033[9m"
    
    END = "\033[0m"

    # Define color codes for different log levels
    LOG_COLORS = {
        'DEBUG': GRAY_BOLD,    # Blue
        'INFO': WHITE_BOLD,     # Grey
        'WARNING': YELLOW_BOLD,  # Yellow
        'ERROR': RED_BOLD,    # Red
        'CRITICAL': PURPLE_BOLD  # Purple
    }
    
    def format(self, record):
        levelname = record.levelname
        sized = levelname[:7] if len(levelname) > 7 else levelname.ljust(7)
        if levelname in self.LOG_COLORS:
            record.levelname = f'{self.LOG_COLORS[levelname]}{sized}{self.END}'
        return super().format(record)


# ===============================


if __name__ == '__main__':
    # With inspection
    log = ValkyrieLogger('info', useInspect = True)
    log.info(1, 1, 'val1,%s,val2,%s' % (10, 20))
    log.info(1, 2, 'val1', 10, 'val2', 20)
    log.info('# This is a test message')
    
    log.debug(1, 1, val1 = 10, val2 = 20)
    log.error('# This is a error message', val1 = 10, val2 = 20)
    
    log.console('info', '# This is a info message')
    log.console('debug', '# This is a debug message')
    log.consoleError('# This is a error message')
    
    # Without inspection
    log = ValkyrieLogger('debug', appName = 'ValkyrieLogger', useInspect = False)
    log.info(1, 1, 'val1,%s,val2,%s' % (10, 20))
    log.info(1, 2, 'val1', 10, 'val2', 20)
    log.info('# This is a test message')
    
    log.debug(1, 1, val1 = 10, val2 = 20)
    log.error('# This is a error message', val1 = 10, val2 = 20)
    
    log.console('info', '# This is a info message')
    log.console('debug', '# This is a debug message')
    log.consoleError('# This is a error message')
