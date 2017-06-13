# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
from copy import deepcopy
from functools import wraps
from itertools import chain
from collections import Mapping, namedtuple
from types import GeneratorType

from .exceptions import TagError

ChildElement = namedtuple('ChildElement', ['name', 'obj'])


class DOMElement():
    """
    Takes care of the tree structure using the "childs" and "parent" attributes
    and manages the DOM manipulation with proper valorization of those two.
    """
    def __init__(self):
        super().__init__()
        self._own_index = None
        self.childs = []
        self.parent = None
        self.content_data = {}

    def _yield_items(self, items, kwitems):
        unnamed = (ChildElement(None, item) for item in items)
        named = (ChildElement(k, v) for k, v in kwitems.items())
        for i, item in enumerate(chain(unnamed, named)):
            if type(item.obj) in (list, tuple, GeneratorType):
                if item.name:
                    # TODO: implement tag named containers
                    # Happens when iterable in kwitems
                    # i.e: d = Div(paragraphs=[P() for _ in range(5)])
                    # d.paragraphs -> [P(), P(), P()...]
                    yield i, item
                else:
                    yield from self._yield_items(item.obj, {})
            elif isinstance(item.obj, DOMElement):
                yield i, item
            else:
                yield i, item

    def content_receiver(reverse=False):
        def _receiver(func):
            @wraps(func)
            def wrapped(inst, *tags, **kwtags):
                for i, tag in inst._yield_items(tags, kwtags):
                    func(inst, i, tag)
                return inst
            return wrapped
        return _receiver

    def _insert(self, name, child, idx=None, prepend=False):
        if idx and idx < 0:
            idx = 0
        if prepend:
            idx = 0
        else:
            idx = idx if idx is not None else len(self.childs)
        self.childs.insert(idx, child)
        if isinstance(child, DOMElement):
            child.parent = self
            child._tab_count = self._tab_count + 1
            child._own_index = self.childs.index(child)
        if name:
            setattr(self, name, child)

    def _find_content(self, cont_name):
        try:
            return self.content_data[cont_name]
        except KeyError:
            if self.parent:
                return self.parent._find_content(cont_name)
            else:
                # TODO: raise no content exception?
                return None

    def inject(self, contents):
        self.content_data.update(contents)

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    @content_receiver()
    def __call__(self, _, tag):
        self._insert(*tag)

    @content_receiver()
    def after(self, i, tag):
        self.parent._insert(*tag, idx=self._own_index + 1 + i)

    @content_receiver(reverse=True)
    def before(self, i, tag):
        self.parent._insert(*tag, idx=self._own_index - i)

    @content_receiver(reverse=True)
    def prepend(self, tag):
        self._insert(child, prepend=True)

    @content_receiver()
    def prepend_to(self, father):
        father.prepend(self)

    @content_receiver()
    def append(self, tag):
        self._insert(tag)

    @content_receiver()
    def append_to(self, father):
        father.append(self)

    def wrap(self, other):
        # TODO: make multiple with content_receiver
        if self.parent:
            self.before(other)
            self.parent.pop(self._own_index)
        return other.append(self)

    def wrap_inner(self, other):
        # TODO
        pass

    def replace_with(self, other):
        # TODO: make multiple with content_receiver
        if isinstance(other, Tag):
            self = other
        else:
            raise TagError()
        return self

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

    def clone(self):
        return deepcopy(self)

    def has(self, pattern):
        # TODO
        # return pattern in self.childs
        pass

    def find(self, id=None, klass=None, tag=None):
        pass


class TagAttrs(dict):
    """
    Html tag attributes container, a subclass of dict with __setitiem__ and update overload.
    Manages the manipulation and render of tag attributes, using the dict api, with few exceptions:
    - space separated multiple value keys
        i.e. the class atrribute, an update on this key will add the value to the list
    - mapping type attributes
        i.e. style attribute, an udpate will trigger the dict.update method

    TagAttrs.render formats all the attributes in the proper html format.
    """
    MAPPING_ATTRS = ('style', )
    MULTI_VALUES_ATTRS = ('klass', 'typ', )
    SPECIALS = {
        'klass': 'class',
        'typ': 'type'
    }
    FORMAT = {
        'style': lambda x: ' '.join('{}: {};'.format(k, v) for k, v in x.items()),
        'klass': lambda x: ' '.join(x),
        'typ': lambda x: ' '.join(x)
    }

    def __setitem__(self, key, value):
        if key in self.MULTI_VALUES_ATTRS:
            if key not in self:
                super().__setitem__(key, [])
            self[key].append(value)
        elif key in self.MAPPING_ATTRS:
            if key not in self:
                super().__setitem__(key, {})
            self[key].update(value)
        else:
            super().__setitem__(key, value)

    def update(self, attrs=None, **kwargs):
        if attrs is not None:
            for k, v in attrs.items() if isinstance(attrs, Mapping) else attrs:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def render(self):
        return ''.join(' {}="{}"'.format(self.SPECIALS.get(k, k),
                                         self.FORMAT.get(k, lambda x: x)(v))
                       for k, v in self.items() if v)


class Tag(DOMElement):
    """
    Provides an api for tag inner manipulation and for rendering.
    """
    _template = '<{tag}{attrs}>{inner}</{tag}>'
    _needed = None
    _void = False

    def __init__(self, **kwargs):
        self.attrs = TagAttrs()
        self.data = {}
        if self._needed and not set(self._needed).issubset(set(kwargs)):
            raise TagError()
        self.attr(**kwargs)
        self._tab_count = 0
        super().__init__()

    @property
    def length(self):
        return len(self.childs)

    @property
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

    def contents(self):
        return self.childs

    def css(self, *props, **kwprops):
        styles = {}
        if props:
            if len(props) == 1 and isinstance(props[0], Mapping):
                styles = props[0]
            elif len(props) == 2:
                styles = dict(*props)
            else:
                raise TagError
        elif kwprops:
            styles = kwprops
        else:
            raise TagError
        return self.attr(attrs={'style': styles})

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
        return ''.join(child.render(pretty) if isinstance(child, DOMElement) else str(child) for child in self.childs)

    def is_a(self, pattern):
        # TODO
        # return true if self == pattern
        pass


class VoidTag(Tag):
    """ A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = '<{tag}{attrs}/>'

class Content(DOMElement):
    """
    Provides the ability to use a simil-tag object as content placeholder
    """
    def __init__(self, name):
        self.name = name
        super().__init__()

    @property
    def content(self):
        return self.parent._find_content(self.name)

    @property
    def length(self):
        return len(self.content)

    def render(self, pretty=False):
        return self.content
