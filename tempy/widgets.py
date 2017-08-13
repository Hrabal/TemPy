# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Widgets
"""
from .tags import Table, Caption, Thead, Tbody, Tfoot, Tr, Th, Td


class TempyTable(Table):
    __tag = Table._Table__tag

    def __init__(self, rows=0, columns=0, data=None, caption=None,
                 head=True, foot=False, **kwargs):
        super().__init__(**kwargs)
        if caption:
            self.append(Caption()(caption))
        if not data:
            data = [[None for _ in range(columns)] for _ in range(rows)]
        if head:
            headers = data[0]
            self(header=Thead()(Tr()(Th()(col) for col in headers)))
            data = data[1:]
        if foot:
            footer = data[-1]
            self(footer=Tfoot()(Td()(Th()(col) for col in footer)))
            data = data[:-1]
        self(body=Tbody()(Tr()(Td()(col) for col in row) for row in data))

    def populate(self, data):
        # TODO: fill the cells / build the structure if empty
        pass
