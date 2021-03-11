# -*- coding: utf-8 -*-
"""@author: Federico Cerchiari <federicocerchiari@gmail.com>
Elements used inside Tempy Classes"""
import re
from copy import copy
try:
    from collections import Mapping
except ImportError:
    from collections.abc import Mapping

from .bases import TempyClass
from .tempy import DOMElement
from .exceptions import WrongContentError, TagError


class Tag(DOMElement):
    """
    Provides an api for tag inner manipulation and for rendering.
    """
    _template = "%s<%s%s>%s%s</%s>"
    _void = False

    def __init__(self, *args, **kwargs):
        data = kwargs.pop("data", {})
        self.attrs = {"style": {}, "klass": set()}
        if args or kwargs:
            self.attr(*args, **kwargs)
        super().__init__(**data)
        self._tab_count = 0

    def _get__tag(self):
        for cls in self.__class__.__mro__:
            try:
                return getattr(self, "_%s__tag" % cls.__name__)
            except AttributeError:
                pass
        raise TagError(self, "_*__tag not defined for this class or bases.")

    def __repr__(self):
        css_repr = "%s%s" % (
            " .css_class (%s)" % (self.attrs["class"])
            if self.attrs.get("class", None)
            else "",
            " .css_id (%s)" % (self.attrs["id"]) if self.attrs.get("id", None) else "",
        )
        return super().__repr__()[:-1] + "%s>" % css_repr

    def __copy__(self):
        new = super().__copy__()
        new.attrs = copy(self.attrs)
        return new

    def attr(self, *args, **kwargs):
        """Add an attribute to the element"""
        for key, value in kwargs.items():
            if key == "klass":
                self.attrs["klass"].update(value.split())
            elif key == "style":
                if isinstance(value, str):
                    splitted = iter(re.split("[;:]", value))
                    value = dict(zip(splitted, splitted))
                self.attrs["style"].update(value)
            else:
                self.attrs[key] = value
        for arg in args:
            self.attrs[arg] = bool
        return self

    def remove_attr(self, attr):
        """Removes an attribute."""
        self.attrs.pop(attr, None)
        return self

    def set_id(self, css_id):
        self.attrs["id"] = css_id
        return self

    def id(self):
        """Returns the tag css id"""
        return self.attrs.get("id", None)

    def is_id(self, css_id):
        """Check if tag have the given id"""
        return css_id == self.id()

    def has_class(self, csscl):
        """Checks if this element have the given css class."""
        return csscl in self.attrs["klass"]

    def toggle_class(self, csscl):
        """Same as jQuery's toggleClass function. It toggles the css class on this element."""
        action = ("add", "remove")[self.has_class(csscl)]
        return getattr(self.attrs["klass"], action)(csscl)

    def add_class(self, cssclass):
        """Adds a css class to this element."""
        if self.has_class(cssclass):
            return self
        return self.toggle_class(cssclass)

    def remove_class(self, cssclass):
        """Removes the given class from this element."""
        if not self.has_class(cssclass):
            return self
        return self.toggle_class(cssclass)

    def css(self, *props, **kwprops):
        """Adds css properties to this element."""
        if props:
            if len(props) == 1 and isinstance(props[0], Mapping):
                styles = props[0]
            else:
                raise WrongContentError(self, props, "Arguments not valid")
        elif kwprops:
            styles = kwprops
        else:
            raise WrongContentError(self, None, "args OR wkargs are needed")
        return self.attr(style=styles)

    def hide(self):
        """Adds the "display: none" style attribute."""
        self.attrs["style"]["display"] = "none"
        return self

    def show(self, display=None):
        """Removes the display style attribute.
        If a display type is provided """
        if not display:
            self.attrs["style"].pop("display")
        else:
            self.attrs["style"]["display"] = display
        return self

    def toggle(self):
        """Same as jQuery's toggle, toggles the display attribute of this element."""
        return self.show() if self.attrs["style"]["display"] == "none" else self.hide()

    def html(self, pretty=False):
        """Renders the inner html of this element."""
        return self.render_childs(pretty=pretty)

    def text(self):
        """Renders the contents inside this element, without html tags."""
        texts = []
        for child in self.childs:
            if isinstance(child, Tag):
                texts.append(child.text())
            elif hasattr(child, "render"):
                texts.append(child.render())
            else:
                texts.append(child)
        return " ".join(texts)

    def render(self, *args, **kwargs):
        """Renders the element and all his childrens."""
        # args kwargs API provided for last minute content injection
        # self._reverse_mro_func('pre_render')
        pretty = kwargs.pop("pretty", False)
        for arg in args:
            if isinstance(arg, dict):
                self.inject(arg)
        if kwargs:
            self.inject(kwargs)

        pretty_pre = pretty_inner = ""
        if pretty:
            pretty_pre = "\n" + ("\t" * self._depth) if pretty else ""
            pretty_inner = "\n" + ("\t" * self._depth) if len(self.childs) > 1 else ""
        inner = self.render_childs(pretty) if not self._void else ""

        tag_data = (
            pretty_pre,
            self._get__tag(),
            self.render_attrs(),
            inner,
            pretty_inner,
            self._get__tag()
        )[: 6 - [0, 3][self._void]]
        return self._template % tag_data

    def apply_function(self, format_function):
        for (index, child) in enumerate(self.childs):
            if child is not None:
                if isinstance(child, TempyClass):
                    child.apply_function(format_function)
                else:
                    self.childs[index] = format_function(self.childs[index])


class VoidTag(Tag):
    """
    A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = "%s<%s%s/>"

    def _insert(self, dom_group, idx=None, prepend=False, name=None):
        raise TagError(self, "Adding elements to a Void Tag is prohibited.")
