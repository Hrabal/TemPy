# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import types
import json
from copy import deepcopy
from collections import Mapping

from exceptions import TagError


class TagContainer(object):

    def __init__(self):
        self.childs = []
        self.parent = None

    def __call__(self, *args):
        return self.append(args)

    def _yield_items(self, items):
        for item in items:
            if type(item) in (
                types.ListType,
                types.TupleType,
                types.GeneratorType,
            ):
                for subitem in item:
                    yield subitem
            else:
                yield item

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def _insert(self, child, idx=None, prepend=False):
        if prepend:
            idx = 0
        else:
            idx = idx or len(self.childs)
        self.childs.insert(idx, child)
        if isinstance(child, Tag):
            child.parent = self
            child._tab_count = self._tab_count + 1
            child._own_index = self.childs.index(child)

    def after(self, *siblings):
        for i, sibling in enumerate(self._yield_items(*siblings)):
            self.parent._insert(sibling, idx=self._own_index + i + 1)
        return self

    def before(self, *siblings):
        for i, sibling in enumerate(self._yield_items(*siblings)):
            self.parent._insert(sibling, idx=self._own_index - i - 1)
        return self

    def prepend(self, *childs):
        for child in self._yield_items(*reversed(childs)):
            self._insert(child, prepend=True)
        return self

    def prepend_to(self, father):
        return father.prepend(self)

    def append(self, *childs):
        for child in self._yield_items(*childs):
            self._insert(child)
        return self

    def append_to(self, father):
        return father.append(self)

    def remove(self):
        self.parent.pop(i=self._own_index)
        return self

    def pop(self, i=0):
        self.childs.pop(i).parent = None
        return self

    def empty(self):
        for child in self.childs:
            self.childs.remove()
        return self

    def children(self):
        return filter(lambda x: isinstance(x, Tag), self.childs)

    def first(self):
        return self.childs[0]

    def last(self):
        return self.childs[-1]

    @property
    def length(self):
        return len(self.childs)

    def next(self):
        return self.parent.child[self._own_index + 1]

    def prev(self):
        return self.parent.child[self._own_index - 1]

    def prev_all(self):
        return self.parent.child[:self._own_index - 1]

    def parent(self):
        return self.parent

    def siblings(self):
        return filter(lambda x: isinstance(x, Tag), self.parent.childs)

    def slice(self, start, end):
        return self.childs[start:end]

    def has(self, pattern):
        # TODO
        # return pattern in self.childs
        pass

    def find(self, pattern):
        # TODO
        # return filter(pattern, self.childs)
        pass


class TagAttrs(dict):
    MAPPING_ATTRS = ('style', )
    MULTI_VALUES_ATTRS = ('klass', 'typ', )
    SPECIALS = {
        'klass': 'class',
        'typ': 'type'
    }
    FORMAT = {
        'style': lambda x: ' '.join('{}: {};'.format(k, v) for k, v in x.iteritems()),
        'klass': lambda x: ' '.join(x) if len(x) > 1 else x,
        'typ': lambda x: ' '.join(x)
    }

    def __setitem__(self, key, value):
        if key in self.MULTI_VALUES_ATTRS:
            if key not in self:
                super(TagAttrs, self).__setitem__(key, [])
            self[key].append(value)
        if key in self.MAPPING_ATTRS:
            if key not in self:
                super(TagAttrs, self).__setitem__(key, {})
            self[key].update(value)
        else:
            super(TagAttrs, self).__setitem__(key, value)

    def update(self, attrs=None, **kwargs):
        if attrs is not None:
            for k, v in attrs.iteritems() if isinstance(attrs, Mapping) else attrs:
                self[k] = v
        for k, v in kwargs.iteritems():
            self[k] = v

    def render(self):
        return ''.join(' {}="{}"'.format(self.SPECIALS.get(k, k),
                                         self.FORMAT.get(k, lambda x: x)(v))
                       for k, v in self.iteritems() if v)


class Tag(TagContainer):
    _template = '<{tag}{attrs}>{inner}</{tag}>'
    _needed = None
    _void = False

    def __init__(self, **kwargs):
        self._own_index = None
        self.attrs = TagAttrs()
        self.data = {}
        if self._needed and not set(self._needed).issubset(set(kwargs)):
            raise TagError()
        self.attr(**kwargs)
        self._tab_count = 0
        super(Tag, self).__init__()

    def index(self):
        return self._own_index

    def attr(self, attrs=None, **kwargs):
        self.attrs.update(attrs or kwargs)
        return self

    def prop(self, other=None, **kwargs):
        return self.attr(other, **kwargs)

    def remove_attr(self, attr):
        self.attrs.pop(attr, None)
        return self

    def remove_prop(self, attr):
        self.attrs.pop(attr, None)
        return self

    def add_class(self, cssclass):
        self.attrs['klass'].append(cssclass)
        return self

    def remove_class(self, cssclass):
        self.attrs['klass'].remove(cssclass)
        return self

    def clone(self):
        return deepcopy(self)

    def remove(self):
        del self

    def contents(self):
        return self.childs

    def css(self):
        # TODO
        pass

    def hide(self):
        self.attrs['style']['display'] = None
        return self

    def show(self):
        self.attrs['style'].pop('display')
        return self

    def toggle(self):
        return self.show() if self.attrs['style']['display'] == None else self.hide()

    def data(self, key, value=None):
        if value:
            self.data[key] = value
            return self
        else:
            return self.data[key]

    def has_class(self, csscl):
        return csscl in self.attrs['klass']

    def toggleClass(self, csscl):
        return self.remove_class(csscl) if self.has_class(csscl) else self.add_class(csscl)

    def html(self):
        return self._render_childs()

    def replace_with(self, other):
        if isinstance(other, Tag):
            self = other
        else:
            raise TagError()
        return self

    def wrap(self, other):
        return self.before(other.append(self)).parent.pop(self._own_index)

    def wrap_inner(self, other):
        self.childs

    def text(self):
        return ''.join(child.text() if isinstance(child, Tag) else child for child in self.childs)

    def render(self, pretty=False):
        prettying = '\t' * self._tab_count + '\n'  # TODO: we're ugly, prettifying don't work
        tag_data = {
            'tag': getattr(self, '_{}__tag'.format(self.__class__.__name__)),
            'attrs': self.attrs.render()
        }
        if not self._void:
            tag_data['inner'] = self._render_childs(pretty)
        template = self._template + prettying if pretty else self._template
        return template.format(**tag_data)

    def _render_childs(self, pretty):
        return ''.join(child.render(pretty) if isinstance(child, Tag) else str(child) for child in self.childs)

    def is_a(self, pattern):
        # TODO
        # return true if self == pattern
        pass


class VoidTag(Tag):
    _void = True
    _template = '<{tag}{attrs}/>'


class TagFinder(object):

    def replace_all(other):
        # TODO replace all finded with other
        pass

    def filter(pattern):
        # TODO find thing with pattern
        pass
