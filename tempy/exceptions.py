# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""


class TempyException(Exception):
    """Base TemPy exception class"""
    def __init__(self, tempy_object, *args):
        super().__init__(*args)
        self.tempy_object = tempy_object


class TagError(TempyException):
    """Base Tag Exception"""


class TagContentError(TagError):
    """Raised when dealing with Content or DOMElement.content_data"""
    def __init__(self, tag, content, *args):
        super().__init__(tag, content, *args)
        self.content = content


class WrongContentError(TagContentError, ValueError):
    """Raised when the provided content is not a dict."""


class WidgetError(TempyException):
    """Base widget error"""


class WidgetDataError(WidgetError):
    """Raised when wrong data is given to a widget"""


class ContentError(TempyException):
    """Base Tag Exception"""
