# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import types

from exceptions import TagError

SPECIAL_ATTRS = {
    'klass': 'class',
    'typ': 'type',
}


class pyQueryFinder(object):

    def __init__(self):
        self.__all_tags = []

    def __add_new_tag(self, tag):
        self.__all_tags.append(tag)

    def __call__(self, pattern):
        find_func = lambda t: True
        if isinstance(pattern, Tag):
            find_func = lambda t: isinstance(t, pattern)
        elif isinstance(pattern, str):
            pattern = pattern.strip()
            if pattern.startswith('.'):
                find_func = lambda t: t.attr.get('klass') == pattern[1:]
            elif pattern.startswith('#'):
                find_func = lambda t: t.attr.get('id') == pattern[1:]
            else:
                tag = getattr(self, '_{}__tag'.format(self.__class__.__name__))
                find_func = lambda t: tag == pattern
        return filter(find_func, self.__all_tags)

pyQ = pyQueryFinder()


class Tag(object):
    _template = '<{tag}{attrs}>{inner}</{tag}>'
    _void = False
    _needed = None

    def __init__(self, **kwargs):
        self.attrs = {}
        if self._needed and not set(self._needed).issubset(set(kwargs)):
            raise TagError()
        self.attr(**kwargs)
        self.childs = []
        self.parent = self._own_index = None
        self._tab_count = 0
        pyQ._pyQueryFinder__add_new_tag(self)

    def __call__(self, *args):
        for arg in args:
            if type(arg) in (
                types.ListType,
                types.TupleType,
                types.GeneratorType,
            ):
                for tag in arg:
                    self.__call__(tag)
            elif isinstance(arg, Tag):
                self._add_to_childs(arg)
            else:
                self.childs.append(arg)
        return self

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def _add_to_childs(self, tag):
        self.childs.append(tag)
        tag.parent = self
        tag._tab_count = self._tab_count + 1
        tag._own_index = self.childs.index(tag)

    def append(self, *childs):
        return self(*childs)

    def append_to(self, father):
        return father.append(self)

    def remove(self):
        self.parent.childs.pop(self._own_index)
        return self

    def pop(self, i=0):
        self.childs.pop(i).parent = None
        return self

    def empty(self):
        for child in self.childs:
            self.childs.remove()
        return self

    def attr(self, **kwargs):
        for karg in kwargs:
            self.attrs[SPECIAL_ATTRS.get(karg, karg)] = kwargs[karg]
        return self

    def find(self, pattern):
        pass

    def render(self, pretty=False):
        prettying = '\t' * self._tab_count + '\n'
        tag_data = {
            'tag': getattr(self, '_{}__tag'.format(self.__class__.__name__)),
            'attrs': ''.join(' {}="{}"'.format(k, v) for k, v in self.attrs.iteritems())
        }
        if not self._void:
            tag_data['inner'] = self._render_childs(pretty)
        template = self._template + prettying if pretty else self._template
        return template.format(**tag_data)

    def _render_childs(self, pretty):
        return ''.join(child.render(pretty) if isinstance(child, Tag) else str(child) for child in self.childs)


class VoidTag(Tag):
    _void = True
    _template = '<{tag}{attrs}/>'
