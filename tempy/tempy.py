# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Main Tempy classes"""
from html import escape
from copy import copy
from numbers import Number

from .bases import TempyClass
from .tempyrepr import REPRFinder
from .modifier import DOMModifier
from .navigator import DOMNavigator
from .exceptions import WrongContentError


class DOMElement(DOMNavigator, DOMModifier, REPRFinder, TempyClass):
    """Takes care of the tree structure using the "childs" and "parent" attributes.
    Manages the DOM manipulation with proper valorization of those two.
    """

    _from_factory = False

    def __init__(self, **kwargs):
        super().__init__()
        self._name = None
        self.childs = []
        if not getattr(self, 'parent', None):
            self.parent = None
        self.content_data = kwargs
        self._stable = True
        for cls in reversed(self.__class__.__mro__[:-6]):
            init = getattr(cls, "init", None)
            if init and init.__name__ in cls.__dict__:
                init(self)

    def __repr__(self):
        return "<%s.%s %s.%s%s%s>" % (
            self.__module__,
            type(self).__name__,
            id(self),
            " Son of %s." % type(self.parent).__name__ if self.parent else "",
            " %d childs." % len(self.childs) if self.childs else "",
            " Named %s" % self._name if self._name else "",
        )

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

    def to_code(self, pretty=False):
        ret = []
        prettying = "\n" + ("\t" * self._depth) if pretty else ""
        childs_to_code = []
        for child in self.childs:
            if issubclass(child.__class__, DOMElement):
                child_code = child.to_code(pretty=pretty)
                childs_to_code.append(child_code)
            else:
                childs_to_code.append('"""%s"""' % child)

        childs_code = ""
        if childs_to_code:
            childs_code = "(%s%s%s)" % (prettying, ", ".join(childs_to_code), prettying)
        class_code = ""
        if self._from_factory:
            class_code += "T."
            if getattr(self, "_void", False):
                class_code += "Void."
        class_code += self.__class__.__name__
        ret.append("%s(%s)%s" % (class_code, self.to_code_attrs(), childs_code))
        return "".join(ret)

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
    def stable(self):
        if all(c.stable for c in self.childs) and self._stable:
            self._stable = True
            return self._stable
        else:
            self._stable = False
            return self._stable

    @property
    def length(self):
        """Returns the number of childs."""
        return len(self.childs)

    @property
    def is_empty(self):
        """True if no childs"""
        return self.length == 0

    def _iter_child_renders(self, pretty=False):
        for child in self.childs:
            if isinstance(child, str):
                yield escape(child)
            elif isinstance(child, Number):
                yield str(child)
            elif issubclass(child.__class__, DOMElement):
                if isinstance(child, Escaped):
                    yield child._render
                else:
                    yield child.render(pretty=pretty)
            elif not issubclass(child.__class__, DOMElement):
                tempyREPR_cls = self._search_for_view(child)
                if tempyREPR_cls:
                    # If there is a TempyREPR class defined in the child class we make a DOMElement out of it
                    # this abomination is used to avoid circular imports
                    class Patched(tempyREPR_cls, DOMElement):
                        def __init__(s, obj, *args, **kwargs):
                            # Forced adoption of the patched element as son of us
                            s.parent = self
                            # MRO would init only the tempyREPR_cls, we force DOMElement init too
                            DOMElement.__init__(s, **kwargs)
                            super().__init__(obj)
                    yield Patched(child).render(pretty=pretty)
                else:
                    yield escape(str(child))

    def render(self, *args, **kwargs):
        """Placeholder for subclass implementation"""
        raise NotImplementedError

    def render_childs(self, pretty=False):
        """Public api to render all the childs using Tempy rules"""
        return "".join(self._iter_child_renders(pretty=pretty))

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
        self._stable = False
        if not contents:
            contents = {}
        if kwargs:
            contents.update(kwargs)
        self.content_data.update(contents)
        return self

    def clone(self):
        """Returns a deepcopy of this element."""
        return copy(self)

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
        self._render = content
