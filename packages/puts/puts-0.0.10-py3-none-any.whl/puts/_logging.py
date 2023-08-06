import logging
import os
from pathlib import Path
from typing import Union

import colorlog


def init_logger(
    log_dir: Union[str, Path] = Path("logs/"),
    stream_only: bool = False,
    reset: bool = True,
):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create the stream handler that logs everything with color to terminal
    sh = colorlog.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # define formatter for the stream handler
    color_log_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s %(black)s(%(filename)s:%(lineno)s)",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "green",
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_yellow",
        },
        secondary_log_colors={},
        style="%",
    )
    sh.setFormatter(color_log_formatter)

    if not stream_only:
        log_dir = Path(log_dir)

        if not log_dir.is_dir():
            os.mkdir(log_dir)
            print("Created directory: {}".format(log_dir))

        debug_log_fp: Path = log_dir / "debug.log"
        error_log_fp: Path = log_dir / "error.log"

        # create the first file handler that records all logs
        fh1 = logging.FileHandler(debug_log_fp, mode="a")
        fh1.setLevel(logging.DEBUG)

        # create the second file handler that records error or more critical logs only
        fh2 = logging.FileHandler(error_log_fp, mode="a")
        fh2.setLevel(logging.ERROR)

        # define formatter for file handlers
        file_log_formatter = logging.Formatter(
            fmt="%(asctime)s\t%(levelname)-8s\t%(filename)s:%(lineno)s\t%(message)s ",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh1.setFormatter(file_log_formatter)
        fh2.setFormatter(file_log_formatter)

    # remove all existing handlers if any
    if reset and logger.hasHandlers():
        logger.handlers = []

    # add colored Stream Handler to the logger
    logger.addHandler(sh)
    # add File Handlers to the logger
    if not stream_only:
        logger.addHandler(fh1)
        logger.addHandler(fh2)

    return logger


get_logger = init_logger

if __name__ == "__main__":
    logger = init_logger(stream_only=True)
    logger.debug("This is a debug message")
    logger.info("This is a message for your information")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical error message")
