# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import sys
import html
import importlib
from uuid import uuid4
from copy import copy
from functools import wraps
from itertools import chain
from operator import attrgetter
from collections import Mapping, OrderedDict, Iterable, ChainMap
from types import GeneratorType, MappingProxyType

from .exceptions import (TagError, WrongContentError, ContentError,
                         WrongArgsError, IncompleteREPRError)


def render_template(template_name, start_directory=None, **kwargs):
    if start_directory:
        sys.path.append(start_directory)
    template_module = importlib.import_module('templates.%s' % template_name)
    template = template_module.template.inject(**kwargs)
    return template.render()


class _ChildElement:
    """Wrapper used to manage element insertion."""

    def __init__(self, name, obj):
        super().__init__()
        if not name and isinstance(obj, (DOMElement, Content)):
            name = obj._name
        self._name = name
        self.obj = obj


class DOMElement:
    """Takes care of the tree structure using the "childs" and "parent" attributes.
    Manages the DOM manipulation with proper valorization of those two.
    """

    def __init__(self):
        super().__init__()
        self._name = None
        self.childs = []
        self.parent = None
        self.content_data = {}
        self.uuid = uuid4().int

    def __repr__(self):
        return '<%s.%s %s.%s%s%s>' % (
            self.__module__,
            type(self).__name__,
            self.uuid,
            ' Son of %s.' % type(self.parent).__name__ if self.parent else '',
            ' %d childs.' % len(self.childs) if self.childs else '',
            ' Named %s' % self._name if self._name else '')

    def __hash__(self):
        return self.uuid

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [{
            'name': t._name,
            'childs': [getattr(c, 'uuid', None) for c in t.childs],
            'content_data': t.content_data,
        } for t in (self, other)]
        return comp_dicts[0] == comp_dicts[1]

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def __next__(self):
        return next(iter(self.childs))

    def __reversed__(self):
        return iter(self.childs[::-1])

    def __len__(self):
        return len(self.childs)

    def __contains__(self, x):
        return x in self.childs

    def __copy__(self):
        return self.__class__()(copy(c) if isinstance(c, (DOMElement, Content)) else c for c in self.childs)

    def __add__(self, other):
        """Addition produces a copy of the left operator, containig the right operator as a child."""
        return self.clone()(other)

    def __iadd__(self, other):
        """In-place addition adds the right operand as left's child"""
        return self(other)

    def __sub__(self, other):
        """Subtraction produces a copy of the left operator, with the right operator removed from left.childs."""
        if other not in self:
            raise ValueError('%s is not in %s' % (other, self))
        ret = self.clone()
        ret.pop(other._own_index)
        return ret

    def __isub__(self, other):
        """removes the child."""
        if other not in self:
            raise ValueError('%s is not in %s' % (other, self))
        return self.pop(other._own_index)

    def __mul__(self, n):
        """Returns a list of clones."""
        if not isinstance(n, int):
            raise TypeError
        if n < 0:
            raise ValueError('Negative multiplication not permitted.')
        return [self.clone() for i in range(n)]

    def __imul__(self, n):
        """Clones the element n times."""
        if not self.parent:
            return self * n
        if n == 0:
            self.parent.pop(self._own_index)
            return self
        return self.after(self * (n-1))

    @property
    def is_root(self):
        return self.root == self

    @property
    def root(self):
        return self.parent.root if self.parent else self

    @property
    def _own_index(self):
        if self.parent:
            try:
                return [t.uuid for t in self.parent.childs].index(self.uuid)
            except ValueError:
                return -1
        return -1

    @property
    def length(self):
        """Returns the number of childs."""
        return len(self.childs)

    @property
    def is_empty(self):
        """True if no childs"""
        return self.length == 0

    def _yield_items(self, items, kwitems, reverse=False):
        """
        Recursive generator, flattens the given items/kwitems.
        Returns index after flattening and a _ChildElement.
        "reverse" parameter inverts the yielding.
        """
        verse = (1, -1)[reverse]
        if isinstance(items, GeneratorType):
            items = list(items)
        unnamed = (_ChildElement(None, item) for item in items[::verse])
        named = (_ChildElement(k, v) for k, v in list(kwitems.items())[::verse])
        contents = (unnamed, named)[::verse]
        for i, item in enumerate(chain(*contents)):
            if type(item.obj) in (list, tuple, GeneratorType):
                if item._name:
                    # TODO: implement tag named containers
                    # Happens when iterable in kwitems
                    # i.e: d = Div(paragraphs=[P() for _ in range(5)])
                    # d.paragraphs -> [P(), P(), P()...]
                    yield i, None, item.obj
                else:
                    yield from self._yield_items(item.obj, {})
            elif isinstance(item.obj, DOMElement):
                item.obj._name = item._name
                yield i, item._name, item.obj
            else:
                yield i, item._name, item.obj

    def _search_for_view(self, obj):
        for item in chain(iter((self.__class__.__name__,
                                self.root.__class__.__name__,
                                'HtmlREPR')),
                          obj.__class__.__dict__):
            found = obj.__class__.__dict__.get(item)
            if found:
                if isinstance(found, type):
                    if issubclass(found, TempyREPR):
                        return found(obj)
        return obj

    def _get_child_renders(self, pretty=False):
        return ''.join(child.render(pretty=pretty) if isinstance(child, (DOMElement, Content, TempyREPR))
                       else html.escape(str(child)) for child in map(self._search_for_view, self.childs))

    def content_receiver(reverse=False):
        """Decorator for content adding methods.
        Takes args and kwargs and calls the decorated method one time for each argument provided.
        The reverse parameter should be used for prepending (relative to self) methods.
        """
        def _receiver(func):
            @wraps(func)
            def wrapped(inst, *tags, **kwtags):
                for i, name, tag in inst._yield_items(tags, kwtags, reverse):
                    inst._stable = False
                    func(inst, i, name, tag)
                return inst
            return wrapped
        return _receiver

    def _insert(self, child, name=None, idx=None, prepend=False):
        """Inserts something inside this element.
        If provided at the given index, if prepend at the start of the childs list, by default at the end.
        If the child is a DOMElement, correctly links the child.
        If a name is provided, an attribute containing the child is created in this instance.
        """
        if child is not None:
            if idx and idx < 0:
                idx = 0
            if prepend:
                idx = 0
            else:
                idx = idx if idx is not None else len(self.childs)
            self.childs.insert(idx, child)
            if isinstance(child, (DOMElement, Content)):
                child.parent = self
                if name:
                    child._name = name
            if name:
                setattr(self, name, child)

    def _find_content(self, cont_name):
        """Search for a content_name in the content data, if not found the parent is searched."""
        try:
            a = self.content_data[cont_name]
            return a
        except KeyError:
            if self.parent:
                return self.parent._find_content(cont_name)
            else:
                # Fallback for no content (Raise NoContent?)
                return ''

    def inject(self, contents=None, **kwargs):
        """
        Adds content data in this element. This will be used in the rendering of this element's childs.
        Multiple injections on the same key will override the content (dict.update behavior).
        """
        if contents and not isinstance(contents, dict):
            raise WrongContentError(self, contents, 'contents should be a dict')
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

    @content_receiver()
    def __call__(self, _, name, child):
        """Calling the object will add the given parameters as childs"""
        self._insert(child, name=name)

    @content_receiver()
    def after(self, i, name, sibling):
        """Adds siblings after the current tag."""
        self.parent._insert(sibling, idx=self._own_index + 1 + i, name=name)
        return self

    @content_receiver(reverse=True)
    def before(self, i, name, sibling):
        """Adds siblings before the current tag."""
        self.parent._insert(sibling, idx=self._own_index - i, name=name)
        return self

    @content_receiver(reverse=True)
    def prepend(self, _, name, child):
        """Adds childs to this tag, starting from the first position."""
        self._insert(child, name=name, prepend=True)
        return self

    def prepend_to(self, father):
        """Adds this tag to a father, at the beginning."""
        father.prepend(self)
        return self

    @content_receiver()
    def append(self, _, name, child):
        """Adds childs to this tag, after the current existing childs."""
        self._insert(child, name=name)
        return self

    def append_to(self, father):
        """Adds this tag to a parent, after the current existing childs."""
        father.append(self)
        return self

    def wrap(self, other):
        """Wraps this element inside another empty tag."""
        # TODO: make multiple with content_receiver
        if other.childs:
            raise TagError(self, 'Wrapping in a non empty Tag is forbidden.')
        if self.parent:
            self.before(other)
            self.parent.pop(self._own_index)
        other.append(self)
        return self

    def wrap_inner(self, other):
        self.move_childs(other)
        self(other)
        return self

    def replace_with(self, other):
        """Replace this element with the given DOMElement."""
        self.after(other)
        self.parent.pop(self._own_index)
        return other

    def remove(self):
        """Detach this element from his father."""
        if self._own_index is not None and self.parent:
            self.parent.pop(self._own_index)
        return self

    def _detach_childs(self, idx_from=None, idx_to=None):
        """Moves all the childs to a new father"""
        idx_from = idx_from or 0
        idx_to = idx_to or len(self.childs)
        removed = self.childs[idx_from: idx_to]
        for child in removed:
            if isinstance(child, (DOMElement, Content)):
                child.parent = None
        self.childs[idx_from: idx_to] = []
        return removed

    def move_childs(self, new_father, idx_from=None, idx_to=None):
        removed = self._detach_childs(idx_from=idx_from, idx_to=idx_to)
        new_father(removed)
        return self

    def move(self, new_father, idx=None, prepend=None, name=None):
        """Moves this element from his father to the given one."""
        self.parent.pop(self._own_index)
        if name:
            self._name = name
        new_father._insert(self, idx=idx, prepend=prepend, name=self._name)
        new_father._stable = False
        return self

    def pop(self, idx=None):
        """Removes the child at given position, if no position is given removes the last."""
        self._stable = False
        if idx is None:
            idx = len(self.childs) - 1
        elem = self.childs.pop(idx)
        if isinstance(elem, DOMElement):
            elem.parent = None
        return elem

    def empty(self):
        """Remove all this tag's childs."""
        self._stable = False
        self._detach_childs()
        return self

    def children(self):
        """Returns Tags and Content Placehorlders childs of this element."""
        return filter(lambda x: isinstance(x, (DOMElement, Content)), self.childs)

    def contents(self):
        """Returns this elements childs list, unfiltered."""
        return self.childs

    def first(self):
        """Returns the first child"""
        return self.childs[0]

    def last(self):
        """Returns the last child"""
        return self.childs[-1]

    def next(self):
        """Returns the next sibling."""
        return self.parent.childs[self._own_index + 1]

    def next_all(self):
        """Returns all the next siblings as a list."""
        return self.parent.childs[self._own_index + 1:]

    def prev(self):
        """Returns the previous sibling."""
        return self.parent.childs[self._own_index - 1]

    def prev_all(self):
        """Returns all the previous siblings as a list."""
        return self.parent.childs[:self._own_index]

    def siblings(self):
        """Returns all the siblings of this element as a list."""
        return list(filter(lambda x: x.uuid != self.uuid, self.parent.childs))

    def get_parent(self):
        """Returns this element's father"""
        return self.parent

    def slice(self, start=None, end=None, step=None):
        """Slice of this element's childs as childs[start:end:step]"""
        return self.childs[start:end:step]

    # TODO: Implement Depth-first traversing with order api
    # def reverse_dfs(self):
    #     """Iterate the tree starting from current element, in reverse depth-first."""
    #     # Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    #     # by D. Eppstein, July 2004.
    #     given = set()
    #     stack = copy(self.childs)
    #     while stack:
    #         tag = stack.pop()
    #         if not tag.childs:
    #             given.add(tag)
    #             yield tag
    #         else:
    #             if set(tag.childs).issubset(given):
    #                 given.add(tag)
    #                 yield tag
    #             else:
    #                 stack.append(tag)
    #                 stack += list(set(tag.childs) - given)
    #     yield self

    # TODO: Implement Breadth-first traversing

    def render(self, *args, **kwargs):
        """Placeholder for subclass implementation"""
        raise NotImplementedError


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
    _MAPPING_ATTRS = ('style', )
    _SET_VALUES_ATTRS = ('klass', )
    _SPECIALS = {
        'klass': 'class',
        'typ': 'type',
        '_for': 'for'
    }
    _FORMAT = {
        'style': lambda x: ' '.join('%s: %s;' % (k, v) for k, v in x.items()),
        'klass': lambda x: ' '.join(x),
        'comment': lambda x: x
    }

    def __init__(self, *args, **kwargs):
        for arg in args:
            if not isinstance(arg, str):
                raise WrongArgsError(self, arg, 'Positional arguments should be strings.')
        super().__init__(**kwargs)
        for boolean_key in args:
            super().__setitem__(boolean_key, bool)
        for key in self._SET_VALUES_ATTRS:
            if key not in self:
                super().__setitem__(key, set())
        for key in self._MAPPING_ATTRS:
            if key not in self:
                super().__setitem__(key, {})

    def __setitem__(self, key, value):
        if key in self._SET_VALUES_ATTRS:
            self[key].add(value)
        elif key in self._MAPPING_ATTRS:
            self[key].update(value)
        else:
            super().__setitem__(key, value)

    def __copy__(self):
        return TagAttrs(**self)

    def update(self, attrs=None, **kwargs):
        if attrs is not None:
            for k, v in attrs.items() if isinstance(attrs, Mapping) else attrs:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def render(self):
        """Renders the tag's attributes using the formats and performing special attributes name substitution."""
        ret = []
        for k, v in self.items():
            if v:
                f_string = (' {}="{}"', ' {}')[v is bool]
                f_args = (self._SPECIALS.get(k, k), self._FORMAT.get(k, lambda x: x)(v))[:2+(v is bool)]
                ret.append(f_string.format(*f_args))
        return ''.join(ret)


class Tag(DOMElement):
    """
    Provides an api for tag inner manipulation and for rendering.
    """
    _template = '{pretty1}<{tag}{attrs}>{pretty2}{inner}{pretty1}</{tag}>'
    _needed_kwargs = None
    _void = False
    default_attributes = {}
    default_data = {}

    def __init__(self, *args, **kwargs):
        super().__init__()
        default_data = copy(self.default_data)
        default_data.update(kwargs.pop('data', {}))
        default_attributes = copy(self.default_attributes)
        default_attributes.update(kwargs)
        self.attrs = TagAttrs()
        self._data = {}
        for k in self._needed_kwargs or []:
            try:
                need_check = default_attributes[k]
            except KeyError:
                need_check = None
            if not need_check:
                raise TagError(self,
                               '%s argument needed for %s' % (k,
                                                              self.__class__))
        self.attr(*args, **default_attributes)
        self.data(**default_data)
        self._tab_count = 0
        self._render = None
        self._stable = True
        self._do_bases_funcs('init')
        if self._void:
            self._render = self.render()

    def _get__tag(self):
        for cls in self.__class__.__mro__:
            try:
                return getattr(self, '_%s__tag' % cls.__name__)
            except AttributeError:
                pass
        raise TagError(self, '_*__tag not defined for this class or bases.')

    def _do_bases_funcs(self, func_name):
        for cls in reversed(self.__class__.__mro__):
            func = getattr(cls, func_name, None)
            if func:
                func(self)

    def __repr__(self):
        css_repr = '%s%s' % (
            ' .css_class %s' % (self.attrs['klass']) if 'klass' in self.attrs else '',
            ' .css_id %s ' % (self.attrs['id']) if 'id' in self.attrs else '',
            )
        return super().__repr__()[:-1] + '%s>' % css_repr

    def __copy__(self):
        new = super().__copy__()
        new.attrs = copy(self.attrs)
        return new

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

    def attr(self, *args, **kwargs):
        """Add an attribute to the element"""
        for arg in args:
            if not isinstance(arg, str):
                raise WrongArgsError(self, arg, 'Positional arguments should be strings.')
        self._stable = False
        kwargs.update({k: bool for k in args})
        self.attrs.update(kwargs)
        return self

    def remove_attr(self, attr):
        """Removes an attribute."""
        self._stable = False
        self.attrs.pop(attr, None)
        return self

    def has_class(self, csscl):
        """Checks if this element have the given css class."""
        return csscl in self.attrs['klass']

    def toggle_class(self, csscl):
        """Same as jQuery's toggleClass function. It toggles the css class on this element."""
        self._stable = False
        action = ('add', 'remove')[self.has_class(csscl)]
        return getattr(self.attrs['klass'], action)(csscl)

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
        self._stable = False
        styles = {}
        if props:
            if len(props) == 1 and isinstance(props[0], Mapping):
                styles = props[0]
            else:
                raise WrongContentError(self, props, 'Arguments not valid')
        elif kwprops:
            styles = kwprops
        else:
            raise WrongContentError(self, None, 'args OR wkargs are needed')
        return self.attr(style=styles)

    def hide(self):
        """Adds the "display: none" style attribute."""
        self._stable = False
        self.attrs['style']['display'] = 'none'
        return self

    def show(self, display=None):
        """Removes the display style attribute.
        If a display type is provided """
        self._stable = False
        if not display:
            self.attrs['style'].pop('display')
        else:
            self.attrs['style']['display'] = display
        return self

    def toggle(self):
        """Same as jQuery's toggle, toggles the display attribute of this element."""
        self._stable = False
        return self.show() if self.attrs['style']['display'] == 'none' else self.hide()

    def data(self, key=None, **kwargs):
        """Adds or retrieve extra data to this element, this data will not be rendered.
        Every tag have a _data attribute (dict), if key is given _data[key] is returned.
        Kwargs are used to udpate this Tag's _data."""
        self._data.update(kwargs)
        if key:
            return self._data[key]
        if not kwargs:
            return self._data
        return self

    def html(self, pretty=False):
        """Renders the inner html of this element."""
        return self._get_child_renders(pretty=pretty)

    def _get_non_tempy_contents(self):
        """Returns rendered Contents and non-DOMElement stuff inside this Tag."""
        for thing in filter(lambda x: not isinstance(x, (DOMElement, Content)), self.childs):
            yield thing

    def text(self):
        """Renders the contents inside this element, without html tags."""
        texts = []
        for child in self.childs:
            if isinstance(child, Tag):
                texts.append(child.text())
            elif isinstance(child, Content):
                texts.append(child.render())
            else:
                texts.append(child)
        return ' '.join(texts)

    def render(self, *args, **kwargs):
        """Renders the element and all his childrens."""
        # args kwargs API provided for last minute content injection
        self._do_bases_funcs('pre_render')
        pretty = kwargs.pop('pretty', False)
        if isinstance(pretty, bool) and pretty:
            pretty1 = 0
            pretty2 = pretty1 + 1
        else:
            pretty1 = pretty2 = False

        for arg in args:
            if isinstance(arg, dict):
                self.inject(arg)
        if kwargs:
            self.inject(kwargs)

        # If the tag or his contents are not changed, we skip all the work
        if self._stable and self._render:
            return self._render

        tag_data = {
            'tag': self._get__tag(),
            'attrs': self.attrs.render(),
            'pretty1': '\n' + ('\t' * pretty1) if pretty else '',
            'pretty2': '\n' + ('\t' * pretty2) if pretty2 else ''
        }
        tag_data['inner'] = self._get_child_renders(pretty2) if not self._void and self.childs else ''

        # We declare the tag is stable and have an official render:
        self._render = self._template.format(**tag_data)
        self._stable = True
        return self._render


class VoidTag(Tag):
    """
    A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = '<{tag}{attrs}/>'


class TempyREPR(DOMElement):
    """Helper Class to provide views for custom objects.
    Objects of classes with a nested TempyREPR subclass are rendered using the TempyREPR subclass as a template.

    """
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        try:
            self.repr()
        except AttributeError:
            raise IncompleteREPRError(self.__class__, 'TempyREPR subclass should implement an "repr" method.')

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__('obj').__getattribute__(attr)
        except:
            return super().__getattribute__(attr)

    def render(self, pretty=False):
        return self._get_child_renders(pretty=pretty)


class Content(DOMElement):
    """
    Provides the ability to use a simil-tag object as content placeholder.
    At render time, a content with the same name is searched in parents, the nearest one is used.
    If no content with the same name is used, an empty string is rendered.
    If instantiated with the named attribute content, this will override all the content injection on parents.
    """
    def __init__(self, name=None, content=None, template=None):
        super().__init__()
        self._tab_count = 0
        if not name and not content:
            raise ContentError(self, 'Content needs at least one argument: name or content')
        self._name = name
        self._fixed_content = content
        self._template = template
        if self._template and not isinstance(self._template, DOMElement):
            raise ContentError(self, 'template argument should be a DOMElement')
        self.uuid = uuid4()
        self.stable = False

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [{
            '_name': t._name,
            'content': list(t.content),
            '_template': t._template,
        } for t in (self, other)]
        return comp_dicts[0] == comp_dicts[1]

    def __copy__(self):
        return self.__class__(self._name, self._fixed_content, self._template)

    @property
    def content(self):
        content = self._fixed_content
        if not content and self.parent:
            content = self.parent._find_content(self._name)
        if isinstance(content, DOMElement) or content:
            if isinstance(content, DOMElement):
                yield content
            elif type(content) in (list, tuple, GeneratorType):
                yield from content
            elif isinstance(content, dict):
                yield content
            elif isinstance(content, str):
                yield content
            else:
                yield from iter([content, ])
        else:
            raise StopIteration

    @property
    def length(self):
        return len(list(self.content))

    def render(self, pretty=False):
        ret = []
        for content in self.content:
            if content is not None:
                if isinstance(content, DOMElement):
                    ret.append(content.render(pretty=pretty))
                else:
                    if self._template:
                        ret.append(self._template.inject(content).render(pretty=pretty))
                    elif isinstance(content, dict):
                        for k, v in content.items():
                            if v is not None:
                                if isinstance(v, list):
                                    ret = ret + [str(i) for i in v if i is not None]
                                else:
                                    ret.append(str(v))
                    else:
                        ret.append(str(content))
        return ' '.join(ret)


class Css(Tag):
    """Special class for the style tag.
    Css attributes can be altered with the .attr Tag api. At render time the attr dict is transformed in valid css:
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
    }
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
    _template = '<style>{css}</style>'

    def __init__(self, *args, **kwargs):
        css_styles = {}
        if args:
            if len(args) > 1:
                raise WrongContentError(self, args, 'Css accepts max one positional argument.')
            if isinstance(args[0], dict):
                css_styles.update(args[0])
            elif isinstance(args[0], Iterable):
                if any(map(lambda x: not isinstance(x, dict), args[0])):
                    raise WrongContentError(self, args, 'Unexpected arguments.')
                css_styles = dict(ChainMap(*args[0]))
        css_styles.update(kwargs)
        super().__init__(css_attrs=css_styles)

    def render(self, *args, **kwargs):
        pretty = kwargs.pop('pretty', False)
        result = []
        nodes_to_parse = [([], self.attrs['css_attrs'])]

        while nodes_to_parse:
            parents, node = nodes_to_parse.pop(0)
            if parents:
                result.append("%s { " % " ".join(parents))
            else:
                parents = []

            for key, value in node.items():
                if isinstance(value, str):
                    result.append('%s: %s; %s' % (key, value, "\n" if pretty else ""))
                elif hasattr(value, '__call__'):
                    result.append('%s: %s; %s' % (key, value(), "\n" if pretty else ""))
                elif isinstance(value, dict):
                    nodes_to_parse.append(([p for p in parents] + [key], value))
            if result:
                result.append("} " + ("\n\n" if pretty else ""))
        return self._template.format(css=''.join(result))
