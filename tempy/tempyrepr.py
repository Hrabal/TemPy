# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Classes used to manage the TempyREPR classes.
TempyREPR classes are nested classes used in custom models/objects,
those are used by Tempy to render instances of those models inside a Tempy tree."""
from functools import partial
from .exceptions import IncompleteREPRError


def _filter_classes(cls_list, cls_type):
    """Filters a list of classes and yields TempyREPR subclasses"""
    for cls in cls_list:
        if isinstance(cls, type) and issubclass(cls, cls_type):
            if cls_type == TempyPlace and cls._base_place:
                pass
            else:
                yield cls


class REPRFinder:
    """Collection of methods used to manage TempyREPR classes."""
    def _evaluate_tempyREPR(self, child, repr_cls):
        """Assign a score ito a TempyRepr class.
        The scores depends on the current scope and position of the object in which the TempyREPR is found."""
        score = 0
        if repr_cls.__name__ == self.__class__.__name__:
            # One point if the REPR have the same name of the container
            score += 1
        elif repr_cls.__name__ == self.root.__class__.__name__:
            # One point if the REPR have the same name of the Tempy tree root
            score += 1

        # Add points defined in scorers methods of used TempyPlaces
        for parent_cls in _filter_classes(repr_cls.__mro__[1:], TempyPlace):
            for scorer in (method for method in dir(parent_cls) if method.startswith('_reprscore')):
                score += getattr(parent_cls, scorer, lambda *args: 0)(parent_cls, self, child)

        return score

    def _search_for_view(self, obj):
        """Searches for TempyREPR class declarations in the child's class.
        If at least one TempyREPR is found, it uses the best one to make a Tempy object.
        Otherwise the original object is returned.
        """
        evaluator = partial(self._evaluate_tempyREPR, obj)
        sorted_reprs = sorted(_filter_classes(obj.__class__.__dict__.values(), TempyREPR), key=evaluator, reverse=True)
        if sorted_reprs:
            # If we find some TempyREPR, we return the one with the best score.
            return sorted_reprs[0]
        return None


class TempyREPR:
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
        except AttributeError:
            return super().__getattribute__(attr)

    def render(self, pretty=False):
        return self.render_childs(pretty=pretty)


class TempyPlace(TempyREPR):
    """Used to identify places in the DOM.
    Everything defined here is a placeholder."""
    _pointer_class = None
    _base_place = True
