import logging
import sys
from pathlib import Path

"""
Logger designed to log to console and, optionally, file. 
If filename specified, saved to file.

Debug flag enables debug level logging to console, else only warning and up.
Debug level is always sent to file.

Mode changes write mode if file logging is enabled.
"""


class DualLogger:
    def __init__(self, name, filename=None, debug=False, mode="a"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # formatter to be used for both streams
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # init stream handler and add to logger
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG if debug else logging.WARNING)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # if filename provided, init handler and add to logger. Else, do nothing.
        if filename:
            #  Check if directory and files exist. Create them if not.
            file_path = Path(f"logs/{filename}")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)
            
            file_handler = logging.FileHandler(file_path, mode=mode, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    # message levels

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)