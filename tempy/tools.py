# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Tools for Tempy
"""
import sys
import importlib
from functools import wraps
from itertools import zip_longest

from .bases import TempyClass


def render_template(template_name, start_directory=None, **kwargs):
    if start_directory:
        sys.path.append(start_directory)
    template_module = importlib.import_module("templates.%s" % template_name)
    template = template_module.template.inject(**kwargs)
    return template.render()


class AdjustableList(list):
    def ljust(self, n, fillvalue=""):
        return self + [fillvalue] * (n - len(self))


def content_receiver(reverse=False):
    """Decorator for content adding methods.
    Takes args and kwargs and calls the decorated method one time for each argument provided.
    The reverse parameter should be used for prepending (relative to self) methods.
    """

    def _receiver(func):
        @wraps(func)
        def wrapped(inst, *tags, **kwtags):
            verse = (1, -1)[int(reverse)]
            kwtags = kwtags.items()
            i = 0
            for typ in (zip_longest((None, ), tags), kwtags)[::verse]:
                for (name, item) in typ:
                    if name and isinstance(item, TempyClass):
                        # Is the DOMGroup is a single DOMElement and we have a name we set his name accordingly
                        item._name = name
                    func(inst, i, item, name)
                    i += 1
            return inst
        return wrapped
    return _receiver
