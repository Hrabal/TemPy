# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Classes for css management"""
import inspect
try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable
from collections import ChainMap

from .elements import Tag
from .tempy import DOMElement
from .exceptions import (
    WrongArgsError,
    WrongContentError,
    AttrNotFoundError,
)


class Css(Tag):
    """Special class for the style tag.
    Css attributes can be altered with the Css.update method. At render time the attr dict is transformed in valid css:
    Css({'html': {
            'body': {
                'color': 'red',
                'div': {
                    'color': 'green',
                    'border': '1px'
                }
            }
        },
        '#myid': {'color': 'blue'}
    })
    translates to:
    <style>
    html body {
        color: red;
    }

    html body div {
        color: green;
        border: 1px;
    }
    #myid {
        'color': 'blue';
    }
    </style>
    """

    _template = "<style>%s</style>"

    def __init__(self, *args, **kwargs):
        css_styles = self._parse__args(*args, **kwargs)
        super().__init__(css_attrs=css_styles)

    def _parse__args(self, *args, **kwargs):
        css_styles = {}

        if len(args) > 1:
            raise WrongContentError(self, args, "Css accepts max one positional argument.")
        if args and isinstance(args[0], dict):
            css_styles.update(args[0])
        elif args and isinstance(args[0], Iterable):
            if any(map(lambda x: not isinstance(x, dict), args[0])):
                raise WrongContentError(self, args, "Unexpected arguments.")
            css_styles = dict(ChainMap(*args[0]))

        css_styles.update(kwargs)
        return css_styles

    def update(self, *args, **kwargs):
        css_styles = self._parse__args(*args, **kwargs)
        self.attrs["css_attrs"].update(css_styles)

    @staticmethod
    def render_dom_element_to_css(element):
        if "id" in element.attrs:
            return "#" + element.attrs["id"]
        if "klass" in element.attrs and element.attrs["klass"]:
            return "." + ".".join(element.attrs["klass"])
        element.attrs["id"] = id(element)
        return "#" + str(id(element))

    @staticmethod
    def _render_tag_to_css(el):
        if el.id() is not None:
            return "#" + str(el.id())
        elif len(el.attrs["klass"]) > 0:
            out = ""
            for klass in el.attrs["klass"]:
                out += "." + klass
            return out
        else:
            return el._get__tag() + " "

    @staticmethod
    def _render_node(node, parents, result, nodes_to_parse, pretty=False):
        for key, value in node.items():
            if isinstance(value, str):
                result.append("%s: %s; %s" % (key, value, "\n" if pretty else ""))
            elif hasattr(value, "__call__"):
                result.append("%s: %s; %s" % (key, value(), "\n" if pretty else ""))
            elif isinstance(value, dict):
                nodes_to_parse.append(([p for p in parents] + [key], value))

    def _render_parents(self, parents, result):
        gen = [parent for parent in parents] if parents else []
        for parent in gen:
            if isinstance(parent, tuple):
                result.append(", ".join(parent))
            elif isinstance(parent, Tag):
                result.append(self._render_tag_to_css(parent))
            elif inspect.isclass(parent):
                result.append(
                    getattr(parent, "_" + parent.__name__ + "__tag") + " "
                )
            elif isinstance(parent, DOMElement):
                result.append(
                    self.__class__.render_dom_element_to_css(parent) + " "
                )
            else:
                result.append("%s " % parent)

    def render(self, *args, **kwargs):
        pretty = kwargs.pop("pretty", False)
        result = []
        nodes_to_parse = [([], self.attrs["css_attrs"])]

        while nodes_to_parse:
            parents, node = nodes_to_parse.pop(0)
            self._render_parents(parents, result)
            result.append("{ ")
            self._render_node(node, parents, result, nodes_to_parse, pretty=pretty)
            if result:
                result.append("} " + ("\n\n" if pretty else ""))
        return self._template % "".join(result)

    def dump(self, filename, **kwargs):
        with open(filename, "w") as file_to_write:
            self._template = "%s"
            file_to_write.write(self.render(**kwargs))
            self._template = "<style>%s</style>"

    def replace_element(self, selector_list, new_style, ignore_error=True):
        if new_style is None or not isinstance(new_style, (str, dict)) or not new_style:
            if ignore_error:
                return
            else:
                raise WrongArgsError(
                    self,
                    new_style,
                    "Second argument should be a non-empty string or dictionary.",
                )

        element_node = self.find_attr(selector_list, ignore_error=ignore_error)
        if element_node is None:
            return
        elif element_node:
            element_node[selector_list[-1]] = new_style
        elif not element_node and selector_list[0] in self.attrs["css_attrs"]:
            (self.attrs["css_attrs"])[selector_list[0]] = new_style

    def find_attr(self, selector_list, ignore_error=True):
        try:
            if not isinstance(selector_list, list) or len(selector_list) < 1:
                raise WrongArgsError(
                    self, selector_list, "The provided argument should be a non-empty list."
                )

            found_node = self.attrs["css_attrs"]
            parent_node = None

            for child in selector_list:
                if child in found_node:
                    parent_node = found_node
                    found_node = found_node[child]
                else:
                    raise AttrNotFoundError(
                        self, selector_list, "Provided element does not exist."
                    )
        except (AttrNotFoundError, WrongArgsError):
            if ignore_error:
                return None
            else:
                raise
        return parent_node

    def clear(self, selector_list=None, ignore_error=True):
        if selector_list is None:
            self.attrs["css_attrs"] = {}
            return

        element_node = self.find_attr(selector_list, ignore_error=ignore_error)
        if element_node is None:
            return
        elif element_node:
            element_node.pop(selector_list[-1], None)
        elif not element_node and selector_list[0] in self.attrs["css_attrs"]:
            (self.attrs["css_attrs"]).pop([selector_list[0]], None)
