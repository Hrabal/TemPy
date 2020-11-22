# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Classes used to manage the TempyREPR classes.
TempyREPR classes are nested classes used in custom models/objects,
those are used by Tempy to render instances of those models inside a Tempy tree."""
from .exceptions import IncompleteREPRError


class TempyREPR:
    """Helper Class to provide views for custom objects.
    Objects of classes with a nested TempyREPR subclass are rendered using the TempyREPR subclass as a template.
    """

    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        try:
            self.repr()
        except AttributeError:
            raise IncompleteREPRError(
                self.__class__, 'TempyREPR subclass should implement an "repr" method.'
            )

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__("obj").__getattribute__(attr)
        except AttributeError:
            return super().__getattribute__(attr)

    def render(self, pretty=False):
        return self.render_childs(pretty=pretty)


class TempyPlace(TempyREPR):
    """Used to identify places in the DOM.
    Everything defined here is a placeholder."""

    _pointer_class = None
    _base_place = True
