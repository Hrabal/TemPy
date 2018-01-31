# -*- coding: utf-8 -*-

from tempy.widgets import TempyTable
from tempy.tags import *
from tempy.elements import Css

data = [['Name', 'Last Name', 'Age', 'Telephone'],
        ['John', 'Doe', '34', '555666777', '444555333'],
        ['Michael', 'Roberts', '22', '555766777', '244555333']]

special_cell = Td()(A(href='python.org'), P()('first paragraph', P()('nested paragraph')))

table1 = TempyTable(rows=3, cols=4, data=data, head=True, caption='User information', width='100%')
table2 = TempyTable(data=data, caption='User information2', width='50%', border='1px solid black')
table3 = TempyTable(data=data, caption='User information3', width='50%')
table4 = TempyTable(data=data, caption='User information4', width='50%')

table2.pop_cell()
special_cell.append_to(table2.childs[0].childs[2])

css_tag = Css({
                '.class_example_1': {'color': 'blue'},
                '.class_example_2': {'color': 'pink'},
                '.class_example_3': {'background-color': 'grey'},
          });

# set class for every cell
table1.col_class('class_example_2')

#applies function to upper string for every cell
table1.map_col(lambda x: x.upper())

# set class for first column of each row
table2.col_class('class_example_1', 0)

#applies function to lower string for second column
table2.map_col(lambda x: x.lower(), 1)

#applies function to upper string for last column
table2.map_col(lambda x: x.upper(), 4)

# set class for every row
table3.row_class('class_example_3')

#applies function to upper string for every row
table3.map_row(lambda x: x.upper())

# set class for second row
table4.row_class('class_example_3', 1)

#applies function to lower string for second row
table4.map_row(lambda x: x.lower(), 1)

#applies col scope to first cell
table1.make_scope(col_scope_list=[(0, 0)])

#applies col scope to last two cells in last row
table4.make_scope(row_scope_list=[(2, 3), (2, 4)])

page = Html()(
    Head()(
        Title()('Tempy - Table example'),
        Meta(charset='utf-8'),
        css_tag
    ),
    body=Body()(
        table1, Br(), Br(),
        table2, Br(), Br(),
        table3, Br(), Br(),
        table4, Br(), Br()
    )
)
