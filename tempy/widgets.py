# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Widgets
"""
from .exceptions import TagError
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

    def __init__(self, rows=0, columns=0, data=None, caption=None,
                 head=True, foot=False, **kwargs):
        super().__init__(**kwargs)
        if caption:
            self.append(Caption()(caption))
        if not data:
            data = [[None for _ in range(columns)]
                    for _ in range(rows + sum((head, foot)))]
        if head:
            headers = data[0]
            self(header=Thead()(Tr()(Th()(col) for col in headers)))
            data = data[1:]
        if foot:
            footer = data[-1]
            self(footer=Tfoot()(Tr()(Td()(col) for col in footer)))
            data = data[:-1]
        self._make_body(data)

    def _make_body(self, data):
        self(body=Tbody()(Tr()(Td()(col) for col in row) for row in data))

    def populate(self, data, force=False):
        """Adds/Replace data in the table, if the data matrix have dimensions different from the existing table structure a TagError is raised.
        data: an iterable of iterables in this form [[col1, col2, col3], [col1, col2, col3]]
        force: if True, changes the size of the table according to the given data
        """
        # TODO: fill the cells / build the structure if empty
        if not force:
            if len(self.childs) == len(data) \
               and max(map(len, self.childs)) == max(map(len, data)):
                raise TagError
        if not self.body:
            self._make_body(data)
        else:
            for t_row, d_row in zip(self.body.childs, data):
                for t_col, d_col in zip(t_row, d_row):
                    t_col.empty()(d_col)
