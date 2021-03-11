# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Classes for DOM building"""
try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable
from copy import copy

from .bases import TempyClass
from .tools import content_receiver
from .exceptions import TagError, WrongArgsError, DOMModByKeyError, DOMModByIndexError


class BaseDOMModifier(TempyClass):
    def _insert(self, dom_group, idx=None, prepend=False, name=None):
        """Inserts a DOMGroup inside this element.
        If provided at the given index, if prepend at the start of the childs list, by default at the end.
        If the child is a DOMElement, correctly links the child.
        If the DOMGroup have a name, an attribute containing the child is created in this instance.
        """
        if dom_group is None:
            return
        if idx and idx < 0:
            idx = 0
        if prepend:
            idx = 0
        if idx is None:
            idx = -1
        if not isinstance(dom_group, Iterable) or isinstance(dom_group, (TempyClass, str)):
            dom_group = [dom_group]
        for i_group, elem in enumerate(dom_group):
            if elem is not None:
                # Element insertion in this DOMElement childs
                if idx == -1:
                    self.childs.append(elem)
                else:
                    self.childs.insert(idx + i_group, elem)
                # Managing child attributes if needed
                if hasattr(elem, "parent"):
                    elem.parent = self
                if name:
                    setattr(self, name, elem)

    @content_receiver()
    def __call__(self, _, child, name=None):
        """Calling the object will add the given parameters as childs"""
        self._insert(child, name=name)

    def clone(self):
        """Returns a deepcopy of this element."""
        return copy(self)


class SiblingsManager(BaseDOMModifier):
    @content_receiver()
    def after(self, i, sibling, name=None):
        """Adds siblings after the current tag."""
        self.parent._insert(sibling, idx=self._own_index + 1 + i, name=name)
        return self

    @content_receiver(reverse=True)
    def before(self, i, sibling, name=None):
        """Adds siblings before the current tag."""
        self.parent._insert(sibling, idx=self._own_index - i, name=name)
        return self


class DOMNihil(SiblingsManager):
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
        removed = self.childs[idx_from:idx_to]
        for child in removed:
            if issubclass(child.__class__, TempyClass):
                child.parent = None
        self.childs[idx_from:idx_to] = []
        return removed

    def move_childs(self, new_father, idx_from=None, idx_to=None):
        removed = self._detach_childs(idx_from=idx_from, idx_to=idx_to)
        new_father(removed)
        return self

    def move(self, new_father, idx=None, prepend=None, name=None):
        """Moves this element from his father to the given one."""
        self.parent.pop(self._own_index)
        new_father._insert(self, idx=idx, prepend=prepend, name=name)
        return self

    def pop(self, arg=None):
        """Removes the child at given position or by name (or name iterator).
            if no argument is given removes the last."""
        if arg is None:
            arg = len(self.childs) - 1
        if isinstance(arg, int):
            try:
                result = self.childs.pop(arg)
            except IndexError:
                raise DOMModByIndexError(self, "Given index invalid.")
            if isinstance(result, TempyClass):
                result.parent = None
        else:
            result = []
            if isinstance(arg, str):
                arg = [arg]
            for x in arg:
                try:
                    result.append(getattr(self, x))
                except AttributeError:
                    raise DOMModByKeyError(self, "Given search key invalid. No child found.")
            for x in result:
                self.childs.remove(x)
                if isinstance(x, TempyClass):
                    x.parent = False
        return result

    def empty(self):
        """Remove all this tag's childs."""
        self._detach_childs()
        return self


class OperatorsModifier(DOMNihil):
    def __add__(self, other):
        """Addition produces a copy of the left operator, containig the right operator as a child."""
        return self.clone()(other)

    def __iadd__(self, other):
        """In-place addition adds the right operand as left's child"""
        return self(other)

    def __sub__(self, other):
        """Subtraction produces a copy of the left operator, with the right operator removed from left.childs."""
        if other not in self:
            raise ValueError("%s is not in %s" % (other, self))
        ret = self.clone()
        ret.pop(other._own_index)
        return ret

    def __isub__(self, other):
        """removes the child."""
        if other not in self:
            raise ValueError("%s is not in %s" % (other, self))
        return self.pop(other._own_index)

    def __mul__(self, n):
        """Returns a list of clones."""
        if not isinstance(n, int):
            raise TypeError
        if n < 0:
            raise ValueError("Negative multiplication not permitted.")
        return [self.clone() for i in range(n)]

    def __imul__(self, n):
        """Clones the element n times."""
        if not self.parent:
            return self * n
        if n == 0:
            self.parent.pop(self._own_index)
            return self
        return self.after(self * (n - 1))


class DOMFather(OperatorsModifier):
    @content_receiver(reverse=True)
    def prepend(self, _, child, name=None):
        """Adds childs to this tag, starting from the first position."""
        self._insert(child, prepend=True, name=name)
        return self

    def prepend_to(self, father):
        """Adds this tag to a father, at the beginning."""
        father.prepend(self)
        return self

    @content_receiver()
    def append(self, _, child, name=None):
        """Adds childs to this tag, after the current existing childs."""
        self._insert(child, name=name)
        return self

    def append_to(self, father):
        """Adds this tag to a parent, after the current existing childs."""
        father.append(self)
        return self


class DOMWrapper(DOMFather):
    def wrap(self, other):
        """Wraps this element inside another empty tag."""
        if other.childs:
            raise TagError(self, "Wrapping in a non empty Tag is forbidden.")
        if self.parent:
            self.before(other)
            self.parent.pop(self._own_index)
        other.append(self)
        return self

    def wrap_many(self, *args, strict=False):
        """Wraps different copies of this element inside all empty tags
        listed in params or param's (non-empty) iterators.
        Returns list of copies of this element wrapped inside args
        or None if not succeeded, in the same order and same structure,
        i.e. args = (Div(), (Div())) -> value = (A(...), (A(...)))
        If on some args it must raise TagError, it will only if strict is True,
        otherwise it will do nothing with them and return Nones on their positions"""
        for arg in args:
            is_elem = arg and isinstance(arg, TempyClass)
            is_elem_iter = (
                not is_elem and arg and isinstance(arg, Iterable) and isinstance(iter(arg).__next__(), TempyClass)
            )
            if not (is_elem or is_elem_iter):
                raise WrongArgsError(self, "%s is not DOMElement nor iterable of DOMElements" % arg)
        wcopies = []
        failures = []

        def wrap_next(tag, idx):
            nonlocal wcopies, failures
            next_copy = self.__copy__()
            try:
                return next_copy.wrap(tag)
            except TagError:
                failures.append(idx)
                return next_copy

        for arg_idx, arg in enumerate(args):
            if isinstance(arg, TempyClass):
                wcopies.append(wrap_next(arg, (arg_idx, -1)))
            else:
                iter_wcopies = []
                for iter_idx, t in enumerate(arg):
                    iter_wcopies.append(wrap_next(t, (arg_idx, iter_idx)))
                wcopies.append(type(arg)(iter_wcopies))

        if failures and strict:
            fail_repr = ', '.join(map(lambda i: str(i[0]) if i[1] == -1 else "[%s - %s]" % i, failures))
            raise TagError(self, "Wrapping in a non empty Tag is forbidden, failed on arguments %s" % fail_repr)
        return wcopies

    def wrap_inner(self, other):
        self.move_childs(other)
        self(other)
        return self


class DOMModifier(DOMWrapper):
    pass
