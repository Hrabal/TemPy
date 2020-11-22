# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Table Widget
"""
from copy import copy
from itertools import zip_longest

import tempy.tags as tags
from ..tools import AdjustableList
from ..exceptions import WidgetDataError


class TempyTable(tags.Table):
    """Table widget.
    Creates a simple table structure using the give data, or an empty table of the given size.self
    params:
    data: an iterable of iterables in this form [[col1, col2, col3], [col1, col2, col3]]
    rows, columns: size of the table if no data is given
    head: if True adds the table header using the first data row
    foot: if True add a table footer using the last data row
    caption: adds the caption to the table
    """
    __tag = tags.Table._Table__tag

    def __init__(self, rows=0, cols=0, data=None, **kwargs):
        caption = kwargs.pop("caption", None)
        head = kwargs.pop("head", False)
        foot = kwargs.pop("foot", False)
        super().__init__(**kwargs)
        self(body=tags.Tbody())
        # Initialize empty data structure if data is not given
        if not data:
            data = [
                [None for _ in range(cols)] for _ in range(rows + sum((head, foot)))
            ]
        else:
            rows = len(data)
            cols = max(map(len, data))
        table_data = copy(data)
        if caption:
            self.make_caption(caption)
        if head and rows > 0:
            self.make_header(table_data.pop(0))
        if foot and rows > 0:
            self.make_footer(table_data.pop())
        if data:
            self.populate(table_data, resize_x=True)

    def _check_row_size(self, row):
        try:
            row_length = len(row)
        except TypeError:
            row_length = row
        if self.body.childs and max(map(len, self.body)) < row_length:
            raise WidgetDataError(self, "The given data has more columns than the table column size.")

    def populate(self, data, resize_x=True, normalize=True):
        """Adds/Replace data in the table.
        data: an iterable of iterables in the form [[col1, col2, col3], [col1, col2, col3]]
        resize_x: if True, changes the x-size of the table according to the given data.
            If False and data have dimensions different from the existing table structure a WidgetDataError is raised.
        normalize: if True all the rows will have the same number of columns, if False, data structure is followed.
        """
        if data is None:
            raise WidgetDataError(
                self,
                "Parameter data should be non-None, to empty the table use TempyTable.clear() or "
                "pass an empty list.",
            )
        data = copy(data)
        if not self.body:
            self(body=tags.Tbody())
        self.clear()

        max_data_x = max(map(len, data))
        if not resize_x:
            self._check_row_size(max_data_x)

        for t_row, d_row in zip_longest(self.body, data):
            if not d_row:
                t_row.remove()
            else:
                if not t_row:
                    t_row = tags.Tr().append_to(self.body)
                if normalize:
                    d_row = AdjustableList(d_row).ljust(max_data_x, None)
                for t_cell, d_cell in zip_longest(t_row, d_row):
                    if not t_cell and resize_x:
                        t_cell = tags.Td().append_to(t_row)
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
        self.body(tags.Tr()(tags.Td()(cell) for cell in row_data))
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
        part_tag, inner_tag = {"header": (tags.Thead, tags.Th), "footer": (tags.Tfoot, tags.Td)}.get(part)
        part_instance = part_tag().append_to(self)
        if not hasattr(self, part):
            setattr(self, part, part_instance)
        return part_instance(tags.Tr()(inner_tag()(col) for col in data))

    def make_header(self, head):
        """Makes the header row from the given data."""
        self._make_table_part("header", head)

    def make_footer(self, footer):
        """Makes the footer row from the given data."""
        self._make_table_part("footer", footer)

    def make_caption(self, caption):
        """Adds/Substitutes the table's caption."""
        if not hasattr(self, "caption"):
            self(caption=tags.Caption())
        return self.caption.empty()(caption)

    def _iter_rows(self, col_index):
        for row in self.body.childs:
            if self.is_col_within_bounds(col_index, row) and row.childs[col_index].childs:
                yield row

    def col_class(self, css_class, col_index=None):
        # adds css_class to every cell
        if col_index is None:
            gen = ((row, cell) for row in self.body.childs for cell in row.childs)
            for (row, cell) in gen:
                cell.attr(klass=css_class)
            return

        for row in self._iter_rows(col_index):
            row.childs[col_index].attr(klass=css_class)

    def row_class(self, css_class, row_index=None):
        # adds css_class to every row
        if row_index is None:
            for row in self.body.childs:
                row.attr(klass=css_class)
        elif self.is_row_within_bounds(row_index):
            self.body.childs[row_index].attr(klass=css_class)

    def map_col(self, col_function, col_index=None, ignore_errors=True):
        # applies function to every cell
        if col_index is None:
            self.map_table(col_function)
            return self

        try:
            for row in self._iter_rows(col_index):
                row.childs[col_index].apply_function(col_function)
        except Exception as ex:
            if ignore_errors:
                pass
            else:
                raise ex

    def map_row(self, row_function, row_index=None, ignore_errors=True):
        # applies function to every row
        if row_index is None:
            self.map_table(row_function)
            return self

        if self.is_row_within_bounds(row_index):
            gen = (
                cell
                for cell in self.body.childs[row_index].childs
                if len(cell.childs) > 0
            )
            self.apply_function_to_cells(gen, row_function, ignore_errors)

    def map_table(self, format_function, ignore_errors=True):
        for row in self.body.childs:
            gen = (cell for cell in row.childs if len(cell.childs) > 0)
            self.apply_function_to_cells(gen, format_function, ignore_errors)

    @staticmethod
    def apply_function_to_cells(gen, format_function, ignore_errors):
        try:
            for cell in gen:
                cell.apply_function(format_function)
        except Exception as ex:
            if ignore_errors:
                pass
            else:
                raise ex

    def make_scope(self, col_scope_list=None, row_scope_list=None):
        """Makes scopes and converts Td to Th for given arguments
        which represent lists of tuples (row_index, col_index)"""
        for scope, itm in ((col_scope_list, "col"), (row_scope_list, "row")):
            if scope is not None and len(scope) > 0:
                self.apply_scope(scope, itm)

    def apply_scope(self, scope_list, scope_tag):
        gen = (
            (row_index, col_index)
            for row_index, col_index in scope_list
            if self.is_row_within_bounds(row_index)
            and self.is_col_within_bounds(col_index, self.body.childs[row_index])
            and len(self.body.childs[row_index].childs[col_index].childs) > 0
        )

        for row_index, col_index in gen:
            cell = self.body.childs[row_index].childs[col_index]
            self.body.childs[row_index].childs[col_index] = tags.Th()(cell.childs[0])
            self.body.childs[row_index].childs[col_index].attrs = copy(cell.attrs)
            self.body.childs[row_index].childs[col_index].attr(scope=scope_tag)

    def is_row_within_bounds(self, row_index):
        if row_index >= 0 and (row_index < len(self.body.childs)):
            return True
        raise WidgetDataError(self, "Row index should be within table bounds")

    def is_col_within_bounds(self, col_index, row):
        if col_index >= 0 and (col_index < len(row.childs)):
            return True
        raise WidgetDataError(self, "Column index should be within table bounds")
