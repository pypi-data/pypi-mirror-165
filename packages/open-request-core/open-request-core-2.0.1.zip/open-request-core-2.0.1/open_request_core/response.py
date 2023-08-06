# coding=utf-8
from __future__ import annotations
import json

__all__ = ["ContentResponse", "DictResponse"]


class ContentResponse(object):
    def __init__(self, content: bytes):
        self._content = content

    @property
    def content(self):
        return self._content

    def __str__(self):
        if self._content is None:
            return "0bytes"
        return "%dbytes" % len(self._content)


class DictResponse(ContentResponse, dict):
    def __init__(self, content: bytes, encoding="utf8"):
        ContentResponse.__init__(self, content)
        self._encoding = encoding
        if content:
            dict.__init__(self, json.loads(content))

    def __str__(self):
        return self.content.decode(self._encoding)


JsonResponse = DictResponse
ByteResponse = ContentResponse
