# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Main Tempy classes"""
import html
from copy import copy
from uuid import uuid4
from itertools import chain
from functools import wraps
from collections import deque
from types import GeneratorType

from .exceptions import TagError, WrongContentError, DOMModByKeyError, DOMModByIndexError
from .tempyrepr import REPRFinder


class _ChildElement:
    """Wrapper used to manage element insertion."""

    def __init__(self, name, obj):
        super().__init__()
        if not name and issubclass(obj.__class__, DOMElement):
            name = obj._name
        self._name = name
        self.obj = obj


class DOMElement(REPRFinder):
    """Takes care of the tree structure using the "childs" and "parent" attributes.
    Manages the DOM manipulation with proper valorization of those two.
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._name = None
        self.childs = []
        self.parent = None
        self.content_data = {}
        self.uuid = uuid4().int
        self._stable = True
        self._data = kwargs
        self._applied_funcs = []
        self._reverse_mro_func('init')

    def _reverse_mro_func(self, func_name):
        for cls in reversed(self.__class__.__mro__):
            func = getattr(cls, func_name, None)
            if func and func not in self._applied_funcs:
                self._applied_funcs.append(func)
                func(self)

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
        return self.__class__()(copy(c) if isinstance(c, DOMElement) else c for c in self.childs)

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

    def _iter_child_renders(self, pretty=False):
        for child in self.childs:
            if not issubclass(child.__class__, DOMElement):
                tempyREPR_cls = self._search_for_view(child)
                if tempyREPR_cls:
                    # If there is a TempyREPR class defined in the child class we make a DOMElement out of it
                    # this trick is used to avoid circular imports
                    class Patched(tempyREPR_cls, DOMElement):
                        pass
                    child = Patched(child)
            try:
                yield child.render(pretty=pretty)
            except (AttributeError, NotImplementedError):
                if isinstance(child, Escaped):
                    yield child._render
                else:
                    yield html.escape(str(child))
            except Exception as ex:
                raise ex

    def render_childs(self, pretty=False):
        """Public api to render all the childs using Tempy rules"""
        return ''.join(self._iter_child_renders(pretty=pretty))

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
            if issubclass(child.__class__, DOMElement):
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

    def _get_non_tempy_contents(self):
        """Returns rendered Contents and non-DOMElement stuff inside this Tag."""
        for thing in filter(lambda x: not issubclass(x.__class__, DOMElement), self.childs):
            yield thing

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
            if issubclass(child.__class__, DOMElement):
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

    def pop(self, arg=None):
        """Removes the child at given position or by name (or name iterator).
            if no argument is given removes the last."""
        self._stable = False
        if arg is None:
            arg = len(self.childs) - 1
        if isinstance(arg, int):
            result = self.childs.pop(arg)
            if isinstance(result, DOMElement):
                result.parent = None
            if result is None:
                raise DOMModByIndexError(self, "Given index invalid.")
        else:
            result = []
            if isinstance(arg, str):
                arg = [arg, ]
            for x in arg:
                try:
                    result.append(getattr(self, x))
                except AttributeError:
                    raise DOMModByKeyError(self, "Given search key invalid. No child found")
            if result:
                for x in result:
                    self.childs.remove(x)
                    if isinstance(x, DOMElement):
                        x.parent = False
        return result

    def empty(self):
        """Remove all this tag's childs."""
        self._stable = False
        self._detach_childs()
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

    def bft(self):
        """ Generator that returns each element of the tree in Breadth-first order"""
        queue = deque([self])
        while queue:
            node = queue.pop()
            yield node
            queue.extendleft(node.childs)

    def dfs_preorder(self, reverse=False):
        """Generator that returns each element of the tree in Preorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        stack.append(self)
        while stack:
            node = stack.pop()
            yield node
            if reverse:
                stack.extend(node.childs)
            else:
                stack.extend(node.childs[::-1])

    def dfs_inorder(self, reverse=False):
        """Generator that returns each element of the tree in Inorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        visited = set()
        visited.add(self)
        if reverse:
            stack.append(self.childs[0])
            stack.append(self)
            stack.extend(self.childs[1:])
        else:
            stack.extend(self.childs[1:])
            stack.append(self)
            stack.append(self.childs[0])
        while stack:
            node = stack.pop()
            if node in visited or not node.childs:
                yield node
            else:
                stack.append(node)
                visited.add(node)
                if reverse:
                    stack.extend(node.childs)
                else:
                    stack.extend(node.childs[::-1])

    def dfs_postorder(self, reverse=False):
        """Generator that returns each element of the tree in Postorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        stack.append(self)
        visited = set()
        while stack:
            node = stack.pop()
            if node in visited:
                yield node
            else:
                visited.add(node)
                stack.append(node)
                if reverse:
                    stack.extend(node.childs)
                else:
                    stack.extend(node.childs[::-1])

    def render(self, *args, **kwargs):
        """Placeholder for subclass implementation"""
        raise NotImplementedError


class Escaped(DOMElement):

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self._render = content
