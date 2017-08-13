# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""


class TempyException(Exception):
    """Base TemPy exception class"""


class TagError(TempyException):
    """Base Tag Exception"""
    def __init__(self, tag, *args):
        super().__init__(*args)
        self.tag = tag


class ContentError(object):
    """Raised when dealing with Content or DOMElement.content_data"""
    def __init__(self, tag, content, *args):
        super().__init__(tag, content, *args)
        self.content = content


class WrongContentError(ContentError, ValueError):
    """Raised when the provided content is not a dict."""
