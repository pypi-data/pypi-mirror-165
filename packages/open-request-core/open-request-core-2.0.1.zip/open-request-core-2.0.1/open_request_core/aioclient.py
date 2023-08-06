#!/usr/bin/env python
# coding=utf-8
from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING
import logging

import aiohttp

from .client import HTTPClient


if TYPE_CHECKING:
    from .request import Request
    from .response import ContentResponse

    TResponse = TypeVar("TResponse", bound=ContentResponse)

__all__ = ["Client"]
logger = logging.getLogger("open-request-core")


class Client(HTTPClient):
    def __init__(self, base_url: str, timeout=3, https_verify=False, max_retries=3):
        super().__init__(base_url, timeout, max_retries)
        self.__https_verify = https_verify

    def open(self):
        self._session = aiohttp.ClientSession()
        self._is_opened = True

    async def close(self):
        if self._is_opened:
            await self._session.close()
        self._is_opened = False

    async def __aenter__(self):
        self.open()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    def get_https_verify(self):
        return self.__https_verify

    async def _handle_single_request(self, request: Request):
        """发送请求

        Args:
            request (Request): Request对象

        Returns:
            tuple: 返回三元组(HTTP status code, HTTP headers, HTTP byte content)
        """
        uri = request.get_uri()
        if self.get_base_url().endswith("/") and uri.startswith("/"):
            url = self.get_base_url() + uri[1:]
        elif not self.get_base_url().endswith("/") and not uri.startswith("/"):
            url = self.get_base_url() + "/" + uri
        else:
            url = self.get_base_url() + uri
        if self._is_opened:
            async with self._session.request(
                method=request.get_method(),
                url=url,
                params=self.get_signed_query_params(request),
                data=request.get_data(),
                headers=self.get_signed_headers(request),
                json=request.get_json(),
                verify_ssl=self.__https_verify,
                timeout=self.get_timeout(),
            ) as resp:
                return resp.status, resp.headers, await resp.read()
        else:
            async with self:
                async with self._session.request(
                    method=request.get_method(),
                    url=url,
                    params=self.get_signed_query_params(request),
                    data=request.get_data(),
                    headers=self.get_signed_headers(request),
                    json=request.get_json(),
                    verify_ssl=self.__https_verify,
                    timeout=self.get_timeout(),
                ) as resp:
                    return resp.status, resp.headers, await resp.read()

    async def do_action(self, request: Request[TResponse]) -> TResponse:
        retries = 0
        while True:
            retries += 1
            logger.debug("client do action send request: {}".format(request))
            status_code, headers, content = await self._handle_single_request(request)
            if retries > self.get_max_retries():
                break
            if self.should_retry(status_code, headers, content):
                continue
            self.should_exception(status_code, headers, content)
            break
        resp = request.resp_cls(content)
        logger.debug("client do action get response: {}".format(resp))
        return resp
