# -*- coding: utf-8 -*-

from tempy.widgets import TempyTable
from tempy.tags import *
from tempy.elements import Css

data = [['Name', 'Last Name', 'Age', 'Telephone'],
        ['John', 'Doe', '34', '555666777', '444555333'],
        ['Michael', 'Roberts', '22', '555766777', '244555333']]

table = TempyTable(rows=3, cols=4, data=data, head=True, caption='User information', width='100%')

table2 = TempyTable(data=data, caption='User information2', width='50%')
table2.pop_cell()

css_tag = Css({
                '.class_example_1': {'color': 'blue'}
          });

# set class for first column of each row
table2.col_class('class_example_1', 0)

page = Html()(
    Head()(
        Title()('Tempy - Table example'),
        Meta(charset='utf-8'),
        css_tag
    ),
    body=Body()(
        table,
        Br(),
        Br(),
        table2
    )
)
