# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Widgets
"""
from itertools import zip_longest

from .tools import AdjustableList
from .exceptions import WidgetDataError
from .tags import Table, Caption, Thead, Tbody, Tfoot, Tr, Th, Td


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
        self.body = None
        # Initialize empty datastructure if data is not given
        if not data:
            data = [[None for _ in range(cols)]
                    for _ in range(rows + sum((head, foot)))]
        if caption:
            self(caption=Caption()(caption))
        if head:
            self(header=Thead()(Tr()(Th()(col) for col in data.pop(0))))
        if foot:
            self(footer=Tfoot()(Tr()(Td()(col) for col in data.pop())))
        self.populate(data, resize_x=True)

    def populate(self, data, resize_x=False, force=True, normalize=True):
        """Adds/Replace data in the table.
        data: an iterable of iterables in the form [[col1, col2, col3], [col1, col2, col3]]
        resize_x: if True, changes the x-size of the table according to the given data.
            If False and data have dimensions different from the existing table structure a WidgetDataError is raised.
        force: if True, overwrites the present data, else fills only the empty cells.
        normalize: if True all the rows will have the same number of columns, if False, data structure is followed.
        """
        if not data:
            # Maybe raise?
            return self
        data_x = max(map(len, data))

        if not self.body:
            # Table is empty
            self(body=Tbody()(Tr()(Td()(col) for col in row) for row in data))
        else:
            if not resize_x:
                if max(map(len, self.body)) < data_x:
                    raise WidgetDataError(self, 'The given data have more columns than the table.')
            for t_row, d_row in zip_longest(self.body, data):
                if not t_row:
                    t_row = Tr()(Td() for _ in range(len(d_row))).append_to(self.body)
                if not d_row and force:
                    t_row.remove()
                else:
                    if normalize:
                        d_row = AdjustableList(d_row).ljust(data_x, None)
                    for t_cell, d_cell in zip_longest(t_row, d_row):
                        if not t_cell and resize_x:
                            t_cell = Td().append_to(t_row)
                        if [d_cell] != t_cell.childs:
                            if force and not t_cell.is_empty:
                                t_cell.empty()
                            if t_cell.is_empty and d_cell is not None:
                                t_cell(d_cell)
        return self
