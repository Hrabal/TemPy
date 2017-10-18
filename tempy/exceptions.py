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


class TagArgsError(TagContentError):
    """Raised when dealing with Tag init args"""


class WrongArgsError(TagArgsError, ValueError):
    """Raised when the provided args are not compliant."""


class WrongContentError(TagContentError, ValueError):
    """Raised when the provided content is not a dict."""


class WidgetError(TempyException):
    """Base widget error"""


class WidgetDataError(WidgetError):
    """Raised when wrong data is given to a widget"""


class ContentError(TempyException):
    """Base Content Exception"""


class REPRError(TempyException):
    """Base TempyREPR Exception"""


class IncompleteREPRError(REPRError, TypeError):
    """Raised when a TempyREPR subclass is not defined correctly."""


class DOMModByIndexError(IndexError, TagError):
    """Raised when wrong index is given to any DOM modification method"""


class DOMModByKeyError(KeyError, TagError):
    """Raised when wrong search key is given to any DOM modification method"""
