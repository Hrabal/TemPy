# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Content class used for rendering with dynamic contents"""
from types import GeneratorType

from .tempy import DOMElement
from .exceptions import ContentError


class Content(DOMElement):
    """
    Provides the ability to use a simil-tag object as content placeholder.
    At render time, a content with the same name is searched in parents, the nearest one is used.
    If no content with the same name is used, an empty string is rendered.
    If instantiated with the named attribute content, this will override all the content injection on parents.
    """
    def __init__(self, name=None, content=None, t_repr=None):
        super().__init__()
        self._tab_count = 0
        if not name and not content:
            raise ContentError(
                self, "Content needs at least one argument: name or content"
            )
        self._name = name
        self._fixed_content = content
        self._t_repr = t_repr
        if self._t_repr and not isinstance(self._t_repr, DOMElement):
            raise ContentError(self, "template argument should be a DOMElement")

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [
            {"_name": t._name, "content": list(t.content), "_t_repr": t._t_repr}
            for t in (self, other)
        ]
        return comp_dicts[0] == comp_dicts[1]

    def __copy__(self):
        return self.__class__(self._name, self._fixed_content, self._t_repr)

    @property
    def content(self):
        content = self._fixed_content
        if not content and self.parent:
            content = self.parent.find_content(self._name)
        if isinstance(content, DOMElement) or content:
            if isinstance(content, DOMElement):
                yield content
            elif isinstance(content, (list, tuple, GeneratorType)):
                yield from content
            elif isinstance(content, dict):
                yield content
            elif isinstance(content, str):
                yield content
            else:
                yield from iter([content])
        else:
            return

    @property
    def length(self):
        return len(list(self.content))

    @staticmethod
    def _render_dict(dct):
        ret = []
        for v in dct.values():
            if isinstance(v, list):
                ret = ret + [str(i) for i in v if i is not None]
            elif v is not None:
                ret.append(str(v))
        return ret

    def render(self, *args, **kwargs):
        pretty = kwargs.pop("pretty", False)
        ret = []
        for content in self.content:
            if content is None:
                continue
            if isinstance(content, DOMElement):
                ret.append(content.render(pretty=pretty))
            elif self._t_repr:
                ret.append(self._t_repr.inject(content).render(pretty=pretty))
            elif isinstance(content, dict):
                ret.extend(self._render_dict(content))
            else:
                ret.append(str(content))
        return " ".join(ret)

    def apply_function(self, format_function):
        for index, content in enumerate(filter(lambda c: c is not None, self.content)):
            if isinstance(content, DOMElement):
                content.apply_function(format_function)
            elif self._t_repr:
                if isinstance(self._t_repr, DOMElement):
                    self._t_repr.apply_function(format_function)
                else:
                    self._t_repr = format_function(self._t_repr)
            elif isinstance(content, dict):
                dict_gen = (key for key in content if content[key] is not None)
                for key in dict_gen:
                    if isinstance(content[key], list):
                        content[key] = [
                            format_function(elem)
                            for elem in content[key]
                            if elem is not None
                        ]
                    else:
                        content[key] = format_function(content[key])
            else:
                self.content[index] = format_function(self.content[index])
