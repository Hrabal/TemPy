# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Main Tempy classes"""
from copy import copy

from .modifier import DOMModifier
from .renderer import TempyRenderer
from .navigator import DOMNavigator
from .exceptions import WrongContentError


class DOMElement(TempyRenderer, DOMNavigator, DOMModifier):
    """Takes care of the tree structure using the "childs" and "parent" attributes.
    Manages the DOM manipulation with proper valorization of those two.
    """

    _from_factory = False

    def __init__(self, **kwargs):
        self._name = None
        self.childs = []
        self.parent = None
        self.content_data = kwargs
        for cls in reversed(self.__class__.__mro__[:-6]):
            init = getattr(cls, "init", None)
            if init and init.__name__ in cls.__dict__:
                init(self)

    def __hash__(self):
        return id(self)

    def __bool__(self):
        # Is it normal that without explicit __bool__ definition
        # custom classes evaluates to False?
        return True

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [
            {
                "name": t._name,
                "childs": [id(c) for c in t.childs if isinstance(c, DOMElement)],
                "content_data": t.content_data,
            }
            for t in (self, other)
        ]
        return comp_dicts[0] == comp_dicts[1]

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def __next__(self):
        return next(iter(self.childs))

    def __reversed__(self):
        return iter(self.childs[::-1])

    def __contains__(self, x):
        return x in self.childs

    def __len__(self):
        return len(self.childs)

    def __copy__(self):
        return self.__class__()(
            copy(c) if isinstance(c, DOMElement) else c for c in self.childs
        )

    @property
    def _depth(self):
        return 0 if self.is_root else self.parent._depth + 1

    @property
    def is_root(self):
        return self.root == self

    @property
    def _own_index(self):
        if self.parent:
            try:
                return [id(t) for t in self.parent.childs].index(id(self))
            except ValueError:
                return -1
        return -1

    @property
    def index(self):
        """Returns the position of this element in the parent's childs list.
        If the element have no parent, returns None.
        """
        return self._own_index

    @property
    def length(self):
        """Returns the number of childs."""
        return len(self.childs)

    @property
    def is_empty(self):
        """True if no childs"""
        return self.length == 0

    def data(self, key=None, **kwargs):
        """Adds or retrieve extra data to this element, this data will not be rendered.
        Every tag have a _data attribute (dict), if key is given _data[key] is returned.
        Kwargs are used to udpate this Tag's _data."""
        self.content_data.update(kwargs)
        if key:
            return self.content_data[key]
        if not kwargs:
            return self.content_data
        return self

    def inject(self, contents=None, **kwargs):
        """
        Adds content data in this element. This will be used in the rendering of this element's childs.
        Multiple injections on the same key will override the content (dict.update behavior).
        """
        if contents and not isinstance(contents, dict):
            raise WrongContentError(self, contents, "contents should be a dict")
        if not contents:
            contents = {}
        if kwargs:
            contents.update(kwargs)
        self.content_data.update(contents)
        return self

    @classmethod
    def join(cls, list_ele):
        n = len(list_ele)
        for index in range(1, 2*n-2, 2):
            list_ele.insert(index, cls())
        return list_ele

    @classmethod
    def map(cls, list_ele):
        mapped_list = [cls()(ele) for ele in list_ele]
        return mapped_list


class Escaped(DOMElement):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.render = content
