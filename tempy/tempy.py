# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
from copy import deepcopy
from functools import wraps
from itertools import chain
from collections import Mapping, namedtuple, OrderedDict
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
        self.childs = []
        self.parent = None
        self.content_data = {}

    @property
    def _own_index(self):
        if self.parent:
            return self.parent.childs.index(self)
        return None
    
    def _yield_items(self, items, kwitems, reverse=None):
        """
        Recursive generator, flattens the given items/kwargs. Returns index after flattening and a ChildElement.
        reverse parameter inverts the yielding.
        """
        unnamed = (ChildElement(None, item) for item in items)
        named = (ChildElement(k, v) for k, v in kwitems.items())
        contents = (items, kwitems)
        if reverse:
            contents = (OrderedDict(list(kwitems.items())[::-1]), items[::-1])
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
        """
        Decorator for content adding methods.
        Takes args and kwargs and calls the decorated method one time for each argument provided.
        The reverse parameter should be used for prepending (relative to self) methods.
        """
        def _receiver(func):
            @wraps(func)
            def wrapped(inst, *tags, **kwtags):
                for i, tag in inst._yield_items(tags, kwtags, reverse):
                    func(inst, i, tag)
                return inst
            return wrapped
        return _receiver

    def _insert(self, name, child, idx=None, prepend=False):
        """
        Inserts something inside this element.
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
        if isinstance(child, DOMElement):
            child.parent = self
            child._tab_count = self._tab_count + 1
        if name:
            setattr(self, name, child)

    def _find_content(self, cont_name):
        """Search for a content_name in the content data, if not found the parent is searched."""
        try:
            return self.content_data[cont_name]
        except KeyError:
            if self.parent:
                return self.parent._find_content(cont_name)
            else:
                # Fallback for no content (Raise NoContent?)
                return ''

    def inject(self, contents, **kwargs):
        """
        Adds content data in this element. This will be used in the rendering of this element's childs.
        Multiple injections on the same key will override the content (dict.update behavior).
        """
        if contents and kwargs:
            contents.update(kwargs)
        self.content_data.update(contents)

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def __len__(self):
        return len(self.childs)

    def __contains__(self, x):
        return x in self.childs
    
    def __copy__(self):
        return deepcopy(self)

    @content_receiver()
    def __call__(self, _, tag):
        """Calling the object will add the given parameters as childs"""
        self._insert(*tag)

    @content_receiver()
    def after(self, i, tag):
        """Adds siblings after the current tag."""
        self.parent._insert(*tag, idx=self._own_index + 1 + i)

    @content_receiver(reverse=True)
    def before(self, i, tag):
        """Adds siblings before the current tag."""
        self.parent._insert(*tag, idx=self._own_index - i)

    @content_receiver(reverse=True)
    def prepend(self, tag):
        """Adds childs tho this tag, starting from the first position."""
        self._insert(child, prepend=True)

    @content_receiver()
    def prepend_to(self, father):
        """Adds this tag to a father, at the beginning."""
        father.prepend(self)

    @content_receiver()
    def append(self, tag):
        """Adds childs tho this tag, after the current existing childs."""
        self._insert(tag)

    @content_receiver()
    def append_to(self, father):
        """Adds this tag to a parent, after the current existing childs."""
        father.append(self)

    def wrap(self, other):
        """Wraps this element inside another empty tag."""
        # TODO: make multiple with content_receiver
        if other.childs:
            raise TagError
        if self.parent:
            self.before(other)
            self.parent.pop(self._own_index)
        return other.append(self)

    def wrap_inner(self, other):
        # TODO
        pass

    def replace_with(self, other):
        """Replace this element with the given DOMElement."""
        # TODO: make multiple with content_receiver
        if isinstance(other, DOMElement):
            self = other
        else:
            raise TagError()
        return self

    def remove(self):
        """Detach this element from his father."""
        self.parent.pop(i=self._own_index)
        return self

    def move(self, new_father, idx=None, prepend=None):
        """Moves this element from his father to the given one."""
        self.parent.pop(i=self._own_index)
        new_father._insert(self.name, self, idx, prepend)
        return self

    def pop(self, idx=None):
        """Removes the child at given position, if no position is given removes the last."""
        if not idx:
            idx = len(self.childs) - 1
        elem = self.childs.pop(idx)
        if isinstance(elem, DOMElement):
            elem.parent = None
        return elem

    def empty(self):
        """Remove all this tag's childs."""
        map(lambda child: self.pop(child._own_index), self.childs)
        return self

    # TODO: Make all the following properties?
    def childrens(self):
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
        return filter(lambda x: x != self, self.parent.childs)

    def parent(self):
        """Returns this element's father"""
        return self.parent

    def slice(self, start=None, end=None, step=None):
        """Slice of this element's childs as childs[start:end:step]"""
        return self.childs[start:end:step]

    def clone(self):
        """Returns a deepcopy of this element."""
        return self.__copy__()

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
    _MAPPING_ATTRS = ('style', )
    _MULTI_VALUES_ATTRS = ('klass', 'typ', )
    _SPECIALS = {
        'klass': 'class',
        'typ': 'type'
    }
    _FORMAT = {
        'style': lambda x: ' '.join('{}: {};'.format(k, v) for k, v in x.items()),
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
            return ''.join(' {}="{}"'.format(self._SPECIALS.get(k, k),
                                             self._FORMAT.get(k, lambda x: x)(v))
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
        """Returns the number of childs."""
        return len(self.childs)

    @property
    def index(self):
        """
        Returns the position of this element in the parent's childs list.
        If the element have no parent, returns None.
        """
        return self._own_index

    def attr(self, attrs=None, **kwargs):
        """Add an attribute to the element"""
        self.attrs.update(attrs or kwargs)
        return self

    def remove_attr(self, attr):
        """Removes an attribute."""
        self.attrs.pop(attr, None)
        return self

    def add_class(self, cssclass):
        """Adds a css class to this element."""
        self.attrs['klass'].append(cssclass)
        return self

    def remove_class(self, cssclass):
        """Removes the given class from this element."""
        self.attrs['klass'].remove(cssclass)
        return self

    def css(self, *props, **kwprops):
        """Adds css properties tho this element."""
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
        self.attrs['style']['display'] = None
        return self

    def show(self):
        """Removes the display style attribute."""
        self.attrs['style'].pop('display')
        return self

    def toggle(self):
        """Same as jQuery's toggle, toggles the display attribute of this element."""
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
        return self.remove_class(csscl) if self.has_class(csscl) else self.add_class(csscl)

    def html(self):
        """Renders the inner html of this element."""
        return self._render_childs()

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

    def render(self, pretty=False):
        """Renders the element and all his childrens."""
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
    """
    A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = '<{tag}{attrs}/>'


class Content(DOMElement):
    """
    Provides the ability to use a simil-tag object as content placeholder.
    At render time, a content with the same name is searched in parents, the nearest one is used.
    If no content with the same name is used, an empty string is rendered.
    If instantiated with the named attribute content, this will override all the content injection on parents.
    """
    def __init__(self, name, content=None):
        self.name = name
        self.parent = None
        self._fixed_content = content
        super().__init__()

    @property
    def content(self):
        return self._fixed_content or self.parent._find_content(self.name)

    @property
    def length(self):
        return len(self.content)

    def render(self, pretty=False):
        return self.content
