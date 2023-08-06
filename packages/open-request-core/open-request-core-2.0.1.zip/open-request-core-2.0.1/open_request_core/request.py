#!/usr/bin/env python
# -*- coding=utf-8 -*-
from typing import Generic, TypeVar, Type
from urllib.parse import urlencode
from .response import ContentResponse

__all__ = ["Request"]

TResponse = TypeVar("TResponse", bound=ContentResponse)


class Request(Generic[TResponse]):
    def __init__(self, method: str, uri: str):
        self.__method = method
        self.__uri = uri
        self.__query_params = {}
        self.__header = {}
        self.__data = None
        self.__json = None
        self.__files = None

    def add_query_param(self, k, v):
        if self.__query_params is None:
            self.__query_params = {}
        self.__query_params[k] = v
        return self

    def get_query_params(self):
        return self.__query_params

    def set_query_params(self, query_params):
        self.__query_params = query_params
        return self

    def get_method(self):
        return self.__method

    def set_method(self, method: str):
        self.__method = method
        return self

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_uri(self):
        return self.__uri

    def set_uri(self, uri: str):
        self.__uri = uri
        return self

    def set_json(self, _json):
        self.__json = _json
        return self

    def get_json(self):
        return self.__json

    def update_json(self, key, value):
        if self.__json is None:
            self.__json = {}
        self.__json[key] = value
        return self

    def set_files(self, files):
        self.__files = files

    def get_files(self):
        return self.__files

    def get_headers(self):
        return self.__header

    def set_headers(self, headers):
        self.__header = headers
        return self

    def add_header(self, k, v):
        if self.__header is None:
            self.__header = dict(k=v)
        else:
            self.__header[k] = v
        return self

    def set_user_agent(self, agent):
        self.add_header("User-Agent", agent)
        return self

    @property
    def resp_cls(self) -> Type[TResponse]:
        return ContentResponse

    def __str__(self):
        s = "{} {}".format(self.__method, self.__uri)
        if self.__query_params:
            s += "?{}".format(urlencode(self.__query_params))
        return s
