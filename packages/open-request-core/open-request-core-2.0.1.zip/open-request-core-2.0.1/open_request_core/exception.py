#!/usr/bin/env python
# coding=utf-8

__all__ = ["ServerException"]


class ServerException(Exception):
    """
    server exception
    """

    def __init__(self, http_status, content):
        Exception.__init__(self)
        self._http_status = http_status
        self._content = content

    def __str__(self):
        return "HTTP Status[{}] Error: {} ".format(
            self._http_status,
            self._content,
        )

    def get_content(self):
        return self._content

    def get_http_status(self):
        return self._http_status
