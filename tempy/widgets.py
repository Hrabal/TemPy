# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Widgets
"""
from copy import copy
from itertools import zip_longest

import tempy.tags as tags
from .tools import AdjustableList
from .exceptions import WidgetDataError, WidgetError
from .tags import Html, Table, Tbody, Thead, Caption
from .tags import Tfoot, Td, Tr, Th, Li, Ul, Dl, Dd, Dt


class TempyPage(Html):
    """HTML Page widget.
    Builds an empty html page with some named common tags:
    - Doctype
    - Head - Title - description meta - keywords meta
    - Body
    Those elements are accessible as page attribute:
    >>> TempyPage.head.charset
    >>> TempyPage.body
    >>> TempyPage.head.title
    Provides an API to manage common meta tags directly.
    """
    __tag = Html._Html__tag

    def __init__(self, title=None, content=None, charset='UTF-8',
                 keywords=None, doctype=None, **kwargs):
        super().__init__(**kwargs)
        self.set_charset(charset)
        self.set_description(content)
        self.set_keywords(keywords or [])

    def init(self):
        self(
            head=tags.Head()(
                charset=tags.Meta(),
                description=tags.Meta(name='description'),
                keywords=tags.Meta(name='keywords'),
                title=tags.Title(),
            ),
            body=tags.Body()
        )

    def set_doctype(self, doctype):
        """Changes the <meta> charset tag (default charset in init is UTF-8)."""
        self.doctype.type_code = doctype
        return self

    def set_charset(self, charset):
        """Changes the <meta> charset tag (default charset in init is UTF-8)."""
        self.head.charset.attr(charset=charset)
        return self

    def set_description(self, description):
        """Changes the <meta> description tag."""
        self.head.description.attr(content=description)
        return self

    def set_keywords(self, keywords):
        """Changes the <meta> keywords tag."""
        self.head.keywords.attr(content=', '.join(keywords))
        return self


class TempyTable(Table):
    """Table widget.
    Creates a simple table structure using the give data, ora an empty table of the given size.self
    params:
    data: an iterable of iterables in this form [[col1, col2, col3], [col1, col2, col3]]
    rows, columns: size of the table if no data is given
    head: if True adds the table header using the first data row
    foot: if True add a table footer using the last data row
    caption: adds the caption to the table
    """
    __tag = Table._Table__tag

    def __init__(self, rows=0, cols=0, data=None, caption=None,
                 head=False, foot=False, **kwargs):
        super().__init__(**kwargs)
        self(body=Tbody())
        # Initialize empty datastructure if data is not given
        if not data:
            data = [[None for _ in range(cols)]
                    for _ in range(rows + sum((head, foot)))]
        if caption:
            self.make_caption(caption)
        if head:
            self.make_header(data.pop(0))
        if foot:
            self.make_footer(data.pop())
        if data:
            self.populate(data, resize_x=True)

    def _check_row_size(self, row):
        try:
            row_lenght = len(row)
        except TypeError:
            row_lenght = row
        if self.body.childs and max(map(len, self.body)) < row_lenght:
            raise WidgetDataError(self, 'The given data have more columns than the table.')

    def populate(self, data, resize_x=True, normalize=True):
        """Adds/Replace data in the table.
        data: an iterable of iterables in the form [[col1, col2, col3], [col1, col2, col3]]
        resize_x: if True, changes the x-size of the table according to the given data.
            If False and data have dimensions different from the existing table structure a WidgetDataError is raised.
        normalize: if True all the rows will have the same number of columns, if False, data structure is followed.
        """
        if data is None:
            raise WidgetDataError(self, 'Parameter data should be non-None, to empty the table use TempyTable.clear() or pass an empty list.')
        data = copy(data)

        if not self.body:
            # Table is empty
            self(body=Tbody())
        self.clear()

        max_data_x = max(map(len, data))
        if not resize_x:
            self._check_row_size(max_data_x)

        for t_row, d_row in zip_longest(self.body, data):
            if not d_row:
                t_row.remove()
            else:
                if not t_row:
                    t_row = Tr().append_to(self.body)
                if normalize:
                    d_row = AdjustableList(d_row).ljust(max_data_x, None)
                for t_cell, d_cell in zip_longest(t_row, d_row):
                    if not t_cell and resize_x:
                        t_cell = Td().append_to(t_row)
                    t_cell.empty()
                    if d_cell is not None:
                        t_cell(d_cell)
        return self

    def clear(self):
        return self.body.empty()

    def add_row(self, row_data, resize_x=True):
        """Adds a row at the end of the table"""
        if not resize_x:
            self._check_row_size(row_data)
        self.body(Tr()(Td()(cell) for cell in row_data))
        return self

    def pop_row(self, idr=None, tags=False):
        """Pops a row, default the last"""
        idr = idr if idr is not None else len(self.body) - 1
        row = self.body.pop(idr)
        return row if tags else [cell.childs[0] for cell in row]

    def pop_cell(self, idy=None, idx=None, tags=False):
        """Pops a cell, default the last of the last row"""
        idy = idy if idy is not None else len(self.body) - 1
        idx = idx if idx is not None else len(self.body[idy]) - 1
        cell = self.body[idy].pop(idx)
        return cell if tags else cell.childs[0]

    def _make_table_part(self, part, data):
        part_tag, inner_tag = {
            'header': (Thead, Th),
            'footer': (Tfoot, Td)
            }.get(part)
        part_instance = part_tag().append_to(self)
        if not hasattr(self, part):
            setattr(self, part, part_instance)
        return part_instance(Tr()(inner_tag()(col) for col in data))

    def make_header(self, head):
        """Makes the header row from the given data."""
        self._make_table_part('header', head)

    def make_footer(self, footer):
        """Makes the footer row from the given data."""
        self._make_table_part('footer', footer)

    def make_caption(self, caption):
        """Adds/Sobstitute the table's caption."""
        if not hasattr(self, 'caption'):
            self(caption=Caption())
        return self.caption.empty()(caption)


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
        self._TempyList__tag = getattr(self._typ, '_%s__tag' % self._typ.__name__)
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
            raise WidgetDataError(self, 'List Input not managed, expected (dict, list), got %s' % type(struct))
        else:
            if self._typ == Dl:
                self.__process_dl_struct(struct)
            else:
                self.__process_li_struct(struct)

        return self

    def __process_li_struct(self, struct):
        for k, submenu in struct.items():
            item = Li()(k)
            self(item)
            if submenu:
                item(TempyList(typ=self._typ, struct=submenu))

    def __process_dl_struct(self, struct):
        for k, submenu in struct.items():
            item = Dt()(k)
            self(item)
            if submenu:
                if isinstance(submenu, (list, set, tuple, dict)):
                    for elem in submenu:
                        self(Dd()(elem))
                else:
                    self(Dd()(submenu))


class TempyList:
    """TempyList is a class factory, it works for both ul and ol lists (TODO: dl).
    See TempyListMeta for TempyList methods and docstings."""
    def __new__(cls, typ=None, struct=None):
        try:
            typ = struct.pop('_typ')
        except (TypeError, KeyError, AttributeError):
            pass
        if isinstance(typ, str):
            try:
                typ = getattr(tags, typ)
            except AttributeError:
                raise WidgetError(cls, 'TempyList type not expected.')
        typ = typ or Ul
        cls_typ = type("TempyList%s" % typ.__name__, (TempyListMeta, typ), {})
        return cls_typ(struct=struct)
