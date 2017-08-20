# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
from uuid import uuid4
from copy import copy
from functools import wraps
from itertools import chain
from operator import attrgetter
from collections import Mapping, OrderedDict, Iterable
from types import GeneratorType, MappingProxyType

from .exceptions import TagError, WrongContentError


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
            'parent': getattr(t.parent, 'uuid', None),
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
        new = self.__class__()(copy(c) if isinstance(c, (DOMElement, Content)) else c for c in self.childs)
        if hasattr(new, 'attrs'):
            new.attrs = self.attrs
        return new

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
    def _own_index(self):
        if self.parent:
            try:
                return [t.uuid for t in self.parent.childs].index(self.uuid)
            except ValueError:
                return -1
        return -1

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

    def move_childs(self, new_father, idx_from=None, idx_to=None):
        """Moves all the childs to a new father"""
        idx_from = idx_from or 0
        idx_to = idx_to or len(self.childs)
        removed = self.childs[idx_from: idx_to]
        self.childs[idx_from: idx_to] = []
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
        for child in self.childs:
            self.pop(child._own_index)
        return self

    def children(self):
        """Returns Tags and Content Placehorlders childs of this element."""
        return filter(lambda x: isinstance(x, DOMElement), self.childs)

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
        return self.parent.child[self._own_index + 1]

    def next_all(self):
        """Returns all the next siblings as a list."""
        return self.parent.child[self._own_index + 1:]

    def prev(self):
        """Returns the previous sibling."""
        return self.parent.child[self._own_index - 1]

    def prev_all(self):
        """Returns all the previous siblings as a list."""
        return self.parent.child[:self._own_index - 1]

    def siblings(self):
        """Returns all the siblings of this element as a list."""
        return filter(lambda x: x.uuid != self.uuid, self.parent.childs)

    def parent(self):
        """Returns this element's father"""
        return self.parent

    def slice(self, start=None, end=None, step=None):
        """Slice of this element's childs as childs[start:end:step]"""
        return self.childs[start:end:step]

    def _dfs_tags(self):
        """Iterate the element inner content, in reverse depth-first.
         Used to render the tags from the childmost ones to the root.
        """
        # Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
        # by D. Eppstein, July 2004.
        given = set()
        stack = copy(self.childs)
        while stack:
            tag = stack.pop()
            if not tag.childs:
                given.add(tag)
                yield tag
            else:
                if set(tag.childs).issubset(given):
                    given.add(tag)
                    yield tag
                else:
                    stack.append(tag)
                    stack += list(set(tag.childs) - given)
        yield self

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
    _MULTI_VALUES_ATTRS = ('klass', 'typ', )
    _SPECIALS = {
        'klass': 'class',
        'typ': 'type'
    }
    _FORMAT = {
        'style': lambda x: ' '.join('%s: %s;' % (k, v) for k, v in x.items()),
        'klass': lambda x: ' '.join(x),
        'typ': lambda x: ' '.join(x),
        'comment': lambda x: x
    }

    def __setitem__(self, key, value):
        if key in self._MULTI_VALUES_ATTRS:
            if key not in self:
                super().__setitem__(key, [])
            self[key].append(value)
        elif key in self._MAPPING_ATTRS:
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
        """Renders the tag's attributes using the formats and performing special attributes name substitution."""
        if hasattr(self, '_comment'):
            # Special case for the comment tag
            return self._comment
        else:
            return ''.join(' %s="%s"' % (self._SPECIALS.get(k, k),
                                         self._FORMAT.get(k, lambda x: x)(v))
                           for k, v in self.items() if v)


class Tag(DOMElement):
    """
    Provides an api for tag inner manipulation and for rendering.
    """
    _template = '{pretty1}<{tag}{attrs}>{pretty2}{inner}{pretty1}</{tag}>'
    _needed_kwargs = None
    _void = False

    def __init__(self, **kwargs):
        super().__init__()
        self.attrs = TagAttrs()
        self.data = {}
        if self._needed_kwargs and not set(self._needed_kwargs).issubset(set(kwargs)):
            raise TagError(self, '%s needed, while %s given' % self._needed_kwargs, kwargs.keys())
        self.attr(**kwargs)
        self._tab_count = 0
        self._render = None
        self._stable = False
        if self._void:
            self._render = self.render()

    def __repr__(self):
        css_repr = '%s%s' % (
            ' .css_class %s' % (self.attrs['klass']) if 'klass' in self.attrs else '',
            ' .css_id %s ' % (self.attrs['id']) if 'id' in self.attrs else '',
            )
        return super().__repr__()[:-1] + '%s>' % css_repr

    @property
    def length(self):
        """Returns the number of childs."""
        return len(self.childs)

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

    def attr(self, attrs=None, **kwargs):
        """Add an attribute to the element"""
        self._stable = False
        self.attrs.update(attrs or kwargs)
        return self

    def remove_attr(self, attr):
        """Removes an attribute."""
        self._stable = False
        self.attrs.pop(attr, None)
        return self

    def add_class(self, cssclass):
        """Adds a css class to this element."""
        self._stable = False
        self.attrs['klass'].append(cssclass)
        return self

    def remove_class(self, cssclass):
        """Removes the given class from this element."""
        self._stable = False
        self.attrs['klass'].remove(cssclass)
        return self

    def css(self, *props, **kwprops):
        """Adds css properties tho this element."""
        self._stable = False
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
        """Adds the "display: none" style attribute."""
        self._stable = False
        self.attrs['style']['display'] = None
        return self

    def show(self):
        """Removes the display style attribute."""
        self._stable = False
        self.attrs['style'].pop('display')
        return self

    def toggle(self):
        """Same as jQuery's toggle, toggles the display attribute of this element."""
        self._stable = False
        return self.show() if self.attrs['style']['display'] == None else self.hide()

    def data(self, key, value=None):
        """Adds extra data to this element, this data will not be rendered."""
        if value:
            self.data[key] = value
            return self
        else:
            return self.data[key]

    def has_class(self, csscl):
        """Checks if this element have the given css class."""
        return csscl in self.attrs['klass']

    def toggle_class(self, csscl):
        """Same as jQuery's toggleClass function. It toggles the css class on this element."""
        self._stable = False
        return self.remove_class(csscl) if self.has_class(csscl) else self.add_class(csscl)

    def html(self):
        """Renders the inner html of this element."""
        return self._get_child_renders()

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
        return ''.join(texts)

    def render(self, *args, **kwargs):
        """Renders the element and all his childrens."""
        # args kwargs API provided for last minute content injection
        pretty = kwargs.pop('pretty', False)
        if pretty:
            pretty1 = 0 if pretty is True else pretty
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
            'tag': getattr(self, '_%s__tag' % self.__class__.__name__),
            'attrs': self.attrs.render(),
            'pretty1': '\n' + ('\t' * pretty1) if pretty else '',
            'pretty2': '\n' + ('\t' * pretty2) if pretty2 else ''
        }
        tag_data['inner'] = self._get_child_renders(pretty1+1) if not self._void and self.childs else ''

        # We declare the tag is stable and have an official render:
        self._render = self._template.format(**tag_data)
        self._stable = True
        return self._render

    def _get_child_renders(self, pretty):
        return ''.join(child.render(pretty=pretty) if isinstance(child, (DOMElement, Content)) else str(child)
                       for child in self.childs if child is not None)


class VoidTag(Tag):
    """
    A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = '<{tag}{attrs}/>'


class Content:
    """
    Provides the ability to use a simil-tag object as content placeholder.
    At render time, a content with the same name is searched in parents, the nearest one is used.
    If no content with the same name is used, an empty string is rendered.
    If instantiated with the named attribute content, this will override all the content injection on parents.
    """
    def __init__(self, name=None, content=None, template=None):
        super().__init__()
        self.parent = None
        self._tab_count = 0
        if not name and not content:
            raise TagError
        self._name = name
        self._fixed_content = content
        self._template = template
        self.uuid = uuid4()
        self.stable = False

    def __repr__(self):
        return '<%s.%s %s.%s%s>' % (
            self.__module__,
            type(self).__name__,
            self.uuid,
            ' Son of %s' % type(self.parent).__name__ if self.parent else '',
            ' Named %s' % self._name if self._name else '')

    def __copy__(self):
        return self.__class__(self._name, self._fixed_content, self._template)

    @property
    def content(self):
        content = self._fixed_content or self.parent._find_content(self._name)
        if content:
            if type(content) in (list, tuple, GeneratorType) or (isinstance(content, Iterable) and content is not str):
                return list(content)
            elif type(content) in (MappingProxyType, ):
                return list(content.values())
            else:
                return (content, )
        else:
            raise StopIteration

    @property
    def length(self):
        return len(self.content)

    def render(self, pretty=False):
        ret = []
        for content in self.content:
            if isinstance(content, DOMElement):
                ret.append(content.render(pretty=pretty))
            else:
                if self._template:
                    ret.append(self._template.inject(content).render(pretty=pretty))
                else:
                    ret.append(str(content))
        return ''.join(ret)


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

    def render(self, *args, **kwargs):
        pretty = kwargs.pop('pretty', False)
        result = []
        nodes_to_parse = [([], self.attrs)]

        while nodes_to_parse:
            parents, node = nodes_to_parse.pop(0)
            if parents:
                result.append("%s { " % " ".join(parents))
            else:
                parents = []

            for key, value in node.items():
                if value.__class__.__name__ in ('str', 'unicode'):
                    result.append('%s: %s; %s' % (key, value, "\n" if pretty else ""))
                elif value.__class__.__name__ == 'function':
                    result.append('%s: %s; %s' % (key, value(), "\n" if pretty else ""))
                elif value.__class__.__name__ == 'dict':
                    nodes_to_parse.append(([p for p in parents] + [key], value))
            if result:
                result.append("}" + "\n\n" if pretty else "")

        return self._template.format(css=''.join(result))
