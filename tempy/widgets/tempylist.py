# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Lists Widget
"""
from itertools import zip_longest

import tempy.tags as tags
from ..exceptions import WidgetError, WidgetDataError


class TempyListMeta:
    """Widget for lists, manages the automatic generation starting from iterables and dicts.
    Plain iterables will produce plain lists, nested dicts will produce nested lists.
    Default list type is unordered. List type (ol, ul or dl) can be passed as
    string argument ("Ul", "Ol", "Dl"),
    list tag classes (tempy.tags.Ul, tempy.tags.Ol) or "_typ" special key in the given structure:
    >>> ul = TempyList()
    >>> ol = TempyList(typ='Ol')
    >>> ol = TempyList(typ=tempy.tags.Ol)
    >>> dl = TempyList(typ=tempy.tags.Dl)
    >>> ol = TempyList(struct={'_typ': tempy.tags.Ol})
    >>> ol = TempyList(struct={'_typ': 'Ol'})
    List building is made through the TempyList.populate method; this will trasform a python datastructure
    (list/tuple/dict/etc..) in a Tempy tree.
    """

    def __init__(self, struct=None):
        self._typ = self.__class__.__bases__[1]
        self._TempyList__tag = getattr(self._typ, "_%s__tag" % self._typ.__name__)
        super().__init__()
        self.populate(struct=struct)

    def populate(self, struct):
        """Generates the list tree.
        struct: if a list/set/tuple is given, a flat list is generated
        <*l><li>v1</li><li>v2</li>...</*l>
        If the list type is 'Dl' a flat list without definitions is generated
        <*l><dt>v1</dt><dt>v2</dt>...</*l>

        If the given struct is a dict, key contaninct lists/tuples/sets/dicts
        will be transformed in nested lists, and so on recursively, using dict
        keys as list items, and dict values as sublists. If type is 'Dl' each
        value will be transformed in definition (or list of definitions)
        except others dict. In that case, it will be transformed in <dfn> tags.

        >>> struct = {'ele1': None, 'ele2': ['sub21', 'sub22'], 'ele3': {'sub31': None, 'sub32': None, '_typ': 'Ol'}}
        >>> TempyList(struct=struct)
        <ul>
            <li>ele1</li>
            <li>ele2
                <ul>
                    <li>sub21</li>
                    <li>sub22</li>
                </ul>
            </li>
            <li>ele3
                <ol>
                    <li>sub31</li>
                    <li>sub32</li>
                </ol>
            </li>
        </ul>
        """

        if struct is None:
            # Maybe raise? Empty the list?
            return self

        if isinstance(struct, (list, set, tuple)):
            struct = dict(zip_longest(struct, [None]))
        if not isinstance(struct, dict):
            raise WidgetDataError(
                self,
                "List Input not managed, expected (dict, list), got %s" % type(struct),
            )
        else:
            if self._typ == tags.Dl:
                self.__process_dl_struct(struct)
            else:
                self.__process_li_struct(struct)

        return self

    def __process_li_struct(self, struct):
        for k, submenu in struct.items():
            item = tags.Li()(k)
            self(item)
            if submenu:
                item(TempyList(typ=self._typ, struct=submenu))

    def __process_dl_struct(self, struct):
        for k, submenu in struct.items():
            item = tags.Dt()(k)
            self(item)
            if submenu:
                if isinstance(submenu, (list, set, tuple, dict)):
                    for elem in submenu:
                        self(tags.Dd()(elem))
                else:
                    self(tags.Dd()(submenu))


class TempyList:
    """TempyList is a class factory, it works for both ul and ol lists (TODO: dl).
    See TempyListMeta for TempyList methods and docstings."""

    def __new__(cls, typ=None, struct=None):
        try:
            typ = struct.pop("_typ")
        except (TypeError, KeyError, AttributeError):
            pass
        if isinstance(typ, str):
            try:
                typ = getattr(tags, typ)
            except AttributeError:
                raise WidgetError(cls, "TempyList type not expected.")
        typ = typ or tags.Ul
        cls_typ = type("TempyList%s" % typ.__name__, (TempyListMeta, typ), {})
        return cls_typ(struct=struct)
