#!/usr/bin/env python
# coding=utf-8
from __future__ import annotations

import http.client as httplib
import json
import logging
from typing import TYPE_CHECKING, TypeVar
from urllib.parse import urlencode, urlparse

from .exception import ServerException

if TYPE_CHECKING:
    from .request import Request
    from .response import ContentResponse

    TResponse = TypeVar("TResponse", bound=ContentResponse)

logger = logging.getLogger("open-request-core")


class HTTPClient(object):
    def __init__(self, base_url: str, timeout=3, max_retries=3):
        self.__base_url = base_url
        self.__timeout = timeout
        self.__max_retries = max_retries
        self._is_opened = False

    def __enter__(self):
        self.open()
        return self

    def open(self):
        parsed_url = urlparse(self.__base_url)
        self._conn = httplib.HTTPConnection(parsed_url.hostname, parsed_url.port, self.__timeout)
        self._conn.connect()
        self._is_opened = True

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self._is_opened:
            self._conn.close()
        self._is_opened = False

    def get_base_url(self):
        return self.__base_url

    def set_base_url(self, base_url: str):
        self.__base_url = base_url

    def get_timeout(self):
        return self.__timeout

    def set_timeout(self, timeout):
        self.__timeout = timeout

    def get_https_verify(self):
        return self.__https_verify

    def get_max_retries(self):
        return self.__max_retries

    def get_signed_headers(self, request: Request):
        return request.get_headers()

    def get_signed_query_params(self, request: Request):
        return request.get_query_params()

    def _handle_single_request(self, request: Request):
        """发送请求

        Args:
            request (Request): Request对象

        Returns:
            tuple: 返回三元组(HTTP status code, HTTP headers, HTTP byte content)
        """
        uri = request.get_uri()
        if self.__base_url.endswith("/") and uri.startswith("/"):
            url = self.__base_url + uri[1:]
        elif not self.__base_url.endswith("/") and not uri.startswith("/"):
            url = self.__base_url + "/" + uri
        else:
            url = self.__base_url + uri
        request_uri = urlparse(url).path
        query_params = self.get_signed_query_params(request)
        if query_params:
            request_uri += "?" + urlencode(query_params)
        body = None
        if request.get_data():
            body = request.get_data()
        elif request.get_json():
            body = json.dumps(request.get_json()).encode("utf-8")
        if self._is_opened:
            self._conn.request(
                method=request.get_method(),
                url=request_uri,
                body=body,
                headers=self.get_signed_headers(request),
            )
            resp = self._conn.getresponse()
            return resp.status, resp.getheaders(), resp.read()
        else:
            with self:
                self._conn.request(
                    method=request.get_method(),
                    url=request_uri,
                    body=body,
                    headers=self.get_signed_headers(request),
                )
                resp = self._conn.getresponse()
                return resp.status, resp.getheaders(), resp.read()

    def do_action(self, request: Request[TResponse]) -> TResponse:
        retries = 0
        while True:
            retries += 1
            logger.debug("client do action send request: {}".format(request))
            status_code, headers, content = self._handle_single_request(request)
            if retries > self.__max_retries:
                break
            if self.should_retry(status_code, headers, content):
                continue
            self.should_exception(status_code, headers, content)
            break
        resp = request.resp_cls(content)
        logger.debug("client do action get response: {}".format(resp))
        return resp

    def should_retry(self, status_code, headers, content) -> bool:
        return False

    def should_exception(self, status_code, headers, content):
        if status_code < 200 or status_code >= 300:
            raise ServerException(status_code, content)


class HTTPSClient(HTTPClient):
    def open(self):
        parsed_url = urlparse(self.get_base_url())
        self._conn = httplib.HTTPSConnection(parsed_url.hostname, parsed_url.port, self.get_timeout())
        self._conn.connect()
        self._is_opened = True
