# open-request-core - This is the core module of standard use for requests

![image](https://img.shields.io/badge/made_in-china-ff2121.svg)
[![image](https://img.shields.io/pypi/v/open-request-core.svg)](https://pypi.org/project/open-request-core/)
[![image](https://img.shields.io/pypi/l/open-request-core.svg)](https://pypi.org/project/open-request-core/)

## About
This is the core module of standard use for requests

## Requirements
- Python3.7

## Install
通过pip命令安装：
```shell
pip install open-request-core
```

## Logging
All log messages by this library are made using the ``DEBUG level``, under the ``open-request-core`` name. On how to control displaying/hiding that please consult the [logging documentation of the standard library](https://docs.python.org/3/howto/logging.html). E.g. to hide these messages you can use:
```shell
logging.getLogger("open-request-core").setLevel(logging.INFO)
```

## Author
- <a href="mailto:pmq2008@gmail.com">Rocky Peng</a>
