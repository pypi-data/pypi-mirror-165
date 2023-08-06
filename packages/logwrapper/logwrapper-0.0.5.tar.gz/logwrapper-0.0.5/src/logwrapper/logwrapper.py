#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: logwrapper.py
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2021-04-25 08:54:08

Description: Generate logger
"""

import logging
import os
from logging import handlers


def loggername_gen(file, tier):
    """Generate the logger name
    Calculate the 'level' based on the project
    name and 'file' name that call this function

    E.g: '/home/example/LogWrapper/utils/util.py'
         'LogWrapper' is the project name
         util.py call this function, tier = 2
         the generated logger name is 'LogWrapper.utils.util'

    :file: str      -- The name of the file to call this function
    :tier: int      -- File tier (relative to the 'Project' folder)
    :returns: str   -- logger name

    """
    # Get the absolute path directory
    absfile = os.path.abspath(file)
    parent = os.path.dirname(absfile)
    # Separate the part with a separator
    dir_list = parent.split(os.path.sep)

    # Specify the value range of level
    if int(tier) > len(dir_list) - 1:
        # Filter out empty strings in the separation result
        r_level = len(dir_list) - 1
    elif 1 <= int(tier) <= len(dir_list) - 1:
        r_level = int(tier)
    else:
        r_level = 1

    # Get the folder name
    connector = '.'
    effect_dir = list()
    # Extract valid folder name
    for lv in range(r_level, 0, -1):
        effect_dir.append(dir_list.pop(-lv))
    dirname = connector.join(effect_dir)

    # Get the file name
    filename = os.path.splitext(os.path.split(file)[1])[0]

    # Get logger_name based on folder name
    logger_name = '{prefix}.{postfix}'.format(prefix=dirname, postfix=filename)

    return logger_name


def setup_logging(config):
    """Initialize the logging module settings

    :conf: dict     -- Initialize parameters
    :return: logger

    """
    LEVEL = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    project = config.get('project', 'Root')  # project name = root logger name
    console = config.get('console', False)  # console output?
    console_level = config.get('console_level', 'DEBUG')  # console log level
    file = config.get('file', True)  # file output?
    file_level = config.get('file_level', 'WARNING')  # file log level
    logfile = config.get('log_file', 'logs/log.log')  # log file save position
    max_size = config.get('max_size', 10240000)  # size of each log file
    backup_count = config.get('backup_count', 10)  # count of log files
    log_format = config.get('format', '%(message)s')  # log format

    # Create and set up a logger
    logger = logging.getLogger(project)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Output to file
    if file:
        # If the log folder does not exist, create it
        dir_path = os.path.dirname(logfile)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Instantiate a rotate file handler
        fh = handlers.RotatingFileHandler(filename=logfile,
                                          mode='a',
                                          maxBytes=max_size,
                                          backupCount=backup_count,
                                          encoding='utf-8')
        fh.setLevel(LEVEL[file_level])
        fh.setFormatter(formatter)

        logger.addHandler(fh)

    # Output to console
    if console:
        # # Instantiate a stream handler
        ch = logging.StreamHandler()
        ch.setLevel(LEVEL[console_level])
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    name = loggername_gen(file=__file__, tier=3)
    print(name)
