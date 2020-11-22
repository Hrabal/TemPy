# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Classes for DOM traversing and accesing"""
import inspect
from collections import deque
from .bases import TempyClass


class DOMNavigator(TempyClass):
    @property
    def root(self):
        return self.parent.root if self.parent else self

    def find_content(self, cont_name):
        """Search for a content_name in the content data, if not found the parent is searched."""
        try:
            a = self.content_data[cont_name]
            return a
        except KeyError:
            if self.parent:
                return self.parent.find_content(cont_name)
            else:
                # Fallback for no content (Raise NoContent?)
                return ""

    def _get_non_tempy_contents(self):
        """Returns rendered Contents and non-DOMElement stuff inside this Tag."""
        for thing in filter(
            lambda x: not issubclass(x.__class__, TempyClass), self.childs
        ):
            yield thing

    @staticmethod
    def _match_selector(el, selector):
        if not selector:
            return True
        if inspect.isclass(selector) and isinstance(el, selector):
            return True
        elif isinstance(selector, str) and (
            (
                inspect.isclass(el) and selector == el.__name__
            ) or selector == el.__class__.__name__
        ):
            return True
        return False

    @staticmethod
    def _match_name(el, name):
        if not name:
            return True
        return name is not None and hasattr(el, "_name") and name == el._name

    def find(self, selector=None, names=None):
        """
        @param:
            selector => css selector / given as list (returns matching elements)
                        or TempyClass name (returns instances of this class)
            names => returns attributes of elements with given name
        """
        found_elements = set()
        for child in self.childs:
            match_selector = self._match_selector(child, selector)
            match_name = self._match_name(child, names)

            if match_name and match_selector:
                found_elements.add(child)

            if issubclass(child.__class__, TempyClass) and child.childs:
                found_elements |= child.find(selector, names)

        return found_elements

    def children(self):
        """Returns Tags and Content Placehorlders childs of this element."""
        return filter(lambda x: isinstance(x, TempyClass), self.childs)

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
        return self.parent.childs[: self._own_index]

    def siblings(self):
        """Returns all the siblings of this element as a list."""
        return list(filter(lambda x: id(x) != id(self), self.parent.childs))

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
            if hasattr(node, "childs"):
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
            _, stack = self.__visit_node(node, stack, reverse)

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
                visited, stack = self.__visit_node(node, stack, reverse, visited)

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
                visited, stack = self.__visit_node(node, stack, reverse, visited)

    @staticmethod
    def __visit_node(node, stack, reverse, visited=None):
        if visited is not None:
            visited.add(node)
            stack.append(node)
        if hasattr(node, "childs"):
            if reverse:
                stack.extend(node.childs)
            else:
                stack.extend(node.childs[::-1])
        return visited, stack
