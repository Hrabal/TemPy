# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Places used by Tempy to choose the right TempyREPR to use.
Magically created starting from the tags module.
"""
import importlib
from .tempyrepr import TempyPlace


class Inside(TempyPlace):
    """Check if a TempyREPR object's container is inside a certain Tempy Tag"""
    def _reprscore_container_parent(self, container, child):
        if container.parent.__class__ == self._pointer_class:
            return 1
        return 0


class Sibling(TempyPlace):
    """Base class for TempyPlaces that depends on the TempyREPR object's container siblings"""
    @classmethod
    def _check_container_siblings(cls, container, start=-1, stop=2):
        container_index = container.parent.childs.index(container)
        before = container.parent.childs[container_index+start:container_index]
        after = container.parent.childs[container_index+1:container_index+stop]
        for sibling in before + after:
            if sibling.__class__ == cls._pointer_class:
                return 1
        return 0


class Near(Sibling):
    """Check if a TempyREPR object's container if near a certain Tempy Tag"""
    def _reprscore_container_siblings(self, container, child):
        return self._check_container_siblings(container)


class Before(Sibling):
    """Check if a TempyREPR object's container if before a certain Tempy Tag"""
    def _reprscore_container_following(self, container, child):
        return self._check_container_siblings(container, start=0)


class After(Sibling):
    """Check if a TempyREPR object's container if after a certain Tempy Tag"""
    def _reprscore_container_previous(self, container, child):
        return self._check_container_siblings(container, stop=0)


# Creation of a TempyPlace class for every tag defined in the tags.py module
all_tags = importlib.import_module('.tags', package='tempy')
for tag in dir(all_tags):
    if not tag.startswith('__'):
        for place_type in (Inside, Near, Before, After):
            place_tag_name = '%s%s' % (place_type.__name__, tag)
            # Dynamic class definition
            place_cls = type(place_tag_name, (place_type, ), {'_pointer_class': getattr(all_tags, tag), '_base_place': False})
            # We put the new dynamically created class inside locals to make it avaiable from the outside
            locals()[place_tag_name] = place_cls
