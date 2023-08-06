# README

<!-- File: README.md -->
<!-- Auther: YJ -->
<!-- Email: yj1516268@outlook.com -->
<!-- Created Time: 2021-04-23 16:46:31 -->

---

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [Example configuration](#example-configuration)
* [Usage](#usage)

<!-- vim-markdown-toc -->

---

Python log wrapper

---

## Example configuration

```toml
[log]
project = 'Project'
console = true
console_level = 'DEBUG'
file = true
file_level = 'INFO'
log_file = 'logs/log.log'
max_size = 10240000
backup_count = 10
format = '%(asctime)s | %(levelname)s | <%(threadName)s> %(module)s.%(funcName)s [%(lineno)d]: %(message)s'
```

- `project`: project name, used to initialize logger
- `console`: whether to output log to STDOUT, use it during debugging, and close it during formal deployment
- `console_level`: log level, optional values are 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
- `file`: whether to output log to file
- `file_level`: log level, optional values are 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
- `log_file`: log file path
- `max_size`: log file size, the unit is KB
- `backup_count`: maximum number of log files
- `format`: format of the log

## Usage

```python
import logging

from logwrapper import logger_name, setup_logging

loggername = logger_name(file=__file__, tier=1)
logger = logging.getLogger(loggername)

logger.info('Action')
```

**NOTE:**

1. The `tier` parent folder of `file` is the `project` name

    E.g: `file = /home/example/Project/src/main.py`, `tier = 2`, return result `loggername = Project.src.main`, namely `project = Project`, which matches the configuration item
