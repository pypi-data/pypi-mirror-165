'''
 #####
#     #  ####   ####  #   ##   #      #      #   #
#       #    # #    # #  #  #  #      #       # #
 #####  #    # #      # #    # #      #        #
      # #    # #      # ###### #      #        #
#     # #    # #    # # #    # #      #        #
 #####   ####   ####  # #    # ###### ######   #

######
#     # ###### ##### ###### #####  #    # # #    # ###### #####
#     # #        #   #      #    # ##  ## # ##   # #      #    #
#     # #####    #   #####  #    # # ## # # # #  # #####  #    #
#     # #        #   #      #####  #    # # #  # # #      #    #
#     # #        #   #      #   #  #    # # #   ## #      #    #
######  ######   #   ###### #    # #    # # #    # ###### #####
'''

import logging
import time
import os

"""
This module contains the SDLogger class and its related functions.
"""


class SDLogger:
    """
    Class used for logging in all scripts

    Attributes:
        _logger (Logger): Access the Logger object from the logging.Logger
            class
    """

    def __init__(self, log_level=None, log_file=True, file_log_level=None,
                 log_file_prefix=None):
        """
        Constructor

        Args:
            log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            log_file (bool, optional): Flag to output a log file
                (Defaults to True)
            file_log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            log_file_prefix(String, optional): Set prefix of log file
                name.

            NOTE: When an SDLogger is instantiated, the name is derived from
            the module, so any subsequent SDLogger instantiation will return a
            reference to the same Logger object.  This could be addressed by
            adding a logger_name parameter, but it may also introduce other issues.

            NOTE: The underlying logging.Logger object root level is set to
            the most verbose input level between log_level and file_log_level,
            so that these two levels are allowed to differ.
        """
        if not os.path.exists('./logs'):
            os.makedirs('./logs')

        date_str = time.strftime('%Y%m%d')
        log_filename = f'./logs/{date_str}.log' if log_file_prefix is None \
            else f'./logs/{log_file_prefix}_{date_str}.log'
        log_vals = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                    'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
        log_level = logging.INFO if log_level is None \
            else log_vals[log_level.upper()]
        file_log_level = log_level if file_log_level is None \
            else log_vals[file_log_level.upper()]
        low_log_level = log_level if (log_level <= file_log_level) \
            else file_log_level
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(low_log_level)

        if not self._logger.hasHandlers():
            screen_format = '%(asctime)s %(levelname)s: %(message)s'
            file_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
            date_format = '[%Y/%m/%d-%H:%M:%S]'
            screen_ch = logging.StreamHandler()
            screen_ch.setLevel(log_level)
            screen_ch.setFormatter(logging.Formatter(screen_format,
                                                     datefmt=date_format))
            self._logger.addHandler(screen_ch)

            if log_file:
                file_ch = logging.FileHandler(log_filename)
                file_ch.setLevel(file_log_level)
                file_ch.setFormatter(logging.Formatter(file_format,
                                                       datefmt=date_format))
                self._logger.addHandler(file_ch)

    def info(self, msg, *args, **kwargs):
        """Logs a message with level INFO on this logger.

        Replicates the info() method provided by the logging.Logger class.

        Args:
            msg (String): The message format string.
            *args: The arguments merged into msg with the string formatting
                operator.
            **kwargs: Optional keyword arguments.
        """
        if self._logger.isEnabledFor(logging.INFO):
            self._logger._log(logging.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Logs a message with level DEBUG on this logger.

        Replicates the debug() method provided by the logging.Logger class.

        Args:
            msg (String): The message format string.
            *args: The arguments merged into msg with the string formatting
                operator.
            **kwargs: Optional keyword arguments.
        """
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger._log(logging.DEBUG, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Logs a message with level WARNING on this logger.

        Replicates the warning() method provided by the logging.Logger class.

        Args:
            msg (String): The message format string.
            *args: The arguments merged into msg with the string formatting
                operator.
            **kwargs: Optional keyword arguments.
        """
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger._log(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Logs a message with level ERROR on this logger.

        Replicates the error() method provided by the logging.Logger class.

        Args:
            msg (String): The message format string.
            *args: The arguments merged into msg with the string formatting
                operator.
            **kwargs: Optional keyword arguments.
        """
        if self._logger.isEnabledFor(logging.ERROR):
            self._logger._log(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """Logs a message with level CRITICAL on this logger.

        Replicates the critical() method provided by the logging.Logger class.

        Args:
            msg (String): The message format string.
            *args: The arguments merged into msg with the string formatting
                operator.
            **kwargs: Optional keyword arguments.
        """
        if self._logger.isEnabledFor(logging.CRITICAL):
            self._logger._log(logging.CRITICAL, msg, args, **kwargs)

    def set_log_level(self, log_level=None):
        """
        Sets the threshold level for this logger's screen messages.

        Derived from the setLevel() method provided by the logging.Logger class.

        Args:
            log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        """
        log_vals = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                    'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
        log_level = logging.INFO if log_level is None \
            else log_vals[log_level.upper()]

        curr_log_level = self._logger.getEffectiveLevel()
        low_log_level = log_level if (log_level <= curr_log_level) \
            else curr_log_level

        self._logger.setLevel(low_log_level)
        self._logger.handlers[0].setLevel(log_level)

    def set_file_log_level(self, file_log_level=None):
        """
        Sets the threshold level for the log file.

        Args:
            file_log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        """
        log_vals = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                    'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
        log_level = self._logger.handlers[0].level
        file_log_level = log_level if file_log_level is None \
            else log_vals[file_log_level.upper()]

        curr_log_level = self._logger.getEffectiveLevel()
        low_log_level = file_log_level if (file_log_level <= curr_log_level) \
            else curr_log_level

        self._logger.setLevel(low_log_level)
        self._logger.handlers[1].setLevel(file_log_level)
