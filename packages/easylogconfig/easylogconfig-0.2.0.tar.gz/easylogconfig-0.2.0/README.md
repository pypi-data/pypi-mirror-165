easylogconfig
=============

This python library provides simple wrapper for standart logging module.

If you want something more than "logging.basicConfig", but don't want to read a lot of
[documentation][1] and write a lot of code.

**WARNING** Since v0.2 python 2 is not supported anymore.

Usage
-----

You can find examples in ./examples directory

```python
import logging
import easylogconfig

log = logging.getLogger(__name__)

# print messages to the stdout, add debug level
easylogconfig.auto(debug=True)
# or print messages to the syslog
easylogconfig.auto(syslog_tag="example_tag")
# or log messages to remote syslog server
easylogconfig.auto(syslog_tag="example_tag", syslog_address=("127.0.0.1", 514))
# or print messages to the file without datetime but with thread names
easylogconfig.auto(file_name="/var/log/example.log", file_backup_count=30,
                   datetime=False, thread=True)

log.info("info message")
log.debug("debug message")

# output format:
# 2019-03-22/10:17:28 INFO    info message
```

Configuration
-------------

Library provides one simple function **auto** with arguments:

* formatter arguments:
  * *debug=False*: add debug messages to output?
  * *thread=False*: add thread names to messages?
  * *datetime=True*: add datetime to messages?
  * *level=False*: add level names to messages?
* [SysLogHandler][2] arguments:
  * **syslog_tag=None**: if set to str, log messages to syslog with this tag
  * *syslog_address="/dev/log"*: syslog server address. By default, it sends syslog messages via
    `/dev/log` file. It can be set to string (ip address or hostname, in this case default 514 port
    is used), or to Tuple[str, int] (like [logging.handlers.SysLogHandler][2])
* [TimedRotatingFileHandler][3] arguments:
  * **file_name=None**: if set to str, log messages to this tile
  * *file_when="midnight"*: file rotating time
  * *file_backup_count=7*: keep last files

Log handlers configuration rules:

* *StreamHandler* will be used if **syslog_tag** or **file_name** are omitted or empty strings
* *SysLogHandler* will be used if **syslog_tag** is set to none-empty string
* *TimedRotatingFileHandler* will be used if **file_name** is set to none-empty string
* *ValueError* will be raised if both **syslog_tag** and **file_name** are set to none-empty string

Installation
------------

```bash
python3 -m pip install -U easylogconfig
# or
python3 -m pip install -U git+https://github.com/tierpod/easylogconfig#egg=easylogconfig
```

Development
-----------

```bash
make venv
source ./venv/bin/activate
(venv) make init-dev init
```

[1]: https://docs.python.org/3.6/howto/logging.html
[2]: https://docs.python.org/3.6/library/logging.handlers.html#logging.handlers.SysLogHandler
[3]: https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
