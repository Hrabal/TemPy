# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Places used by Tempy to choose the right TempyREPR to use.
Magically created starting from the tags module.
"""
import importlib
from .tempyrepr import TempyPlace


class Inside(TempyPlace):
    def _container_lookup(self, container, child):
        if container.parent == self._pointer_class:
            return True
        return False


class Near(TempyPlace):
    def _container_lookup(self, container, child):
        own_index = self._content_index(container, child)
        for sibling in container.childs[own_index - 1:own_index + 1]:
            if sibling.__class__ == self._pointer_class:
                return True
        return False


class Before(TempyPlace):
    def _container_lookup(self, container, child):
        own_index = self._content_index(container, child)
        if container.childs[own_index + 1].__class__ == self._pointer_class:
            return True
        return False


class After(TempyPlace):
    def _container_lookup(self, container, child):
        own_index = self._content_index(container, child)
        if container.childs[own_index - 1].__class__ == self._pointer_class:
            return True
        return False


# Creation of a TempyPlace class for every tag defined in the tags.py module
all_tags = importlib.import_module('.tags', package='tempy')
for tag in dir(all_tags):
    if not tag.startswith('__'):
        for place_type in (Inside, Near, Before, After):
            place_tag_name = '%s%s' % (place_type.__name__, tag)
            place_cls = type(place_tag_name, (place_type, ), {'_pointer_class': getattr(all_tags, tag)})
            # We put the new dynamically created class inside locals to make it avaiable from the outside
            locals()[place_tag_name] = place_cls
