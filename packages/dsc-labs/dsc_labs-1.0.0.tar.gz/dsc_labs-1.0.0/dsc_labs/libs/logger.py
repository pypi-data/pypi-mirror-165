#! /usr/bin/env python3

import logging

from bugsnag.handlers import BugsnagHandler


class DSCLabsLogger:
    """
    Initialize and return a logger instance

    Optionally, adds a bugsnag handler. The handler reports log events
    for error levels ERROR and above.
    """
    def __init__(self, default_handler=False) -> None:
        log_format = ('time="%(asctime)-15s" module=%(module)s '
                      'level=%(levelname)-7s %(message)s')
        self.default_handler = default_handler
        logging.basicConfig(format=log_format)
        # For lambda functions
        if len(logging.getLogger().handlers):
            handler = logging.getLogger().handlers[0]
            handler.setFormatter(logging.Formatter(log_format))
        # Enable INFO logs for dsc_labs libs and apps only
        self.logger_instance = logging.getLogger(__name__)
        self.logger_instance.setLevel(logging.INFO)
        logging.getLogger('dsc_labs').setLevel(logging.INFO)

    @staticmethod
    def get_bugsnag_handler() -> BugsnagHandler:
        handler = BugsnagHandler()
        # Notify only ERROR levels and above.
        handler.setLevel(logging.ERROR)
        return handler

    def get_logger(self) -> logging.Logger:
        if self.default_handler:
            return self.logger_instance
        bugsnag_handler = self.get_bugsnag_handler()
        self.logger_instance.addHandler(bugsnag_handler)
        return self.logger_instance


class DSCLabsLoggerMixin:
    def __init__(self) -> None:
        mll = DSCLabsLogger(default_handler=True)
        self.log = mll.get_logger()


class DSCLabsAPILoggerMixin:
    def __init__(self) -> None:
        mll = DSCLabsLogger()
        self.log = mll.get_logger()
