# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from copy import copy

from tempy.widgets import TempyTable, TempyList
from tempy.tags import Table, Tr, Td, Ul, Ol, Li

from tempy.exceptions import WidgetDataError


class TestTempyTable(unittest.TestCase):

    def setUp(self):
        self.data = [[x*y for x in range(1, 11)] for y in range(15)]

    def verify_content(self, table):
        # Check table content
        self.assertTrue(0 in table.body[0][4])
        self.assertTrue(1 in table.body[1][0])
        self.assertTrue(2 in table.body[1][1])
        self.assertTrue(16 in table.body[8][1])

    def test_empty_creation(self):
        table = TempyTable()
        self.assertFalse(table.body)
        # Future non-regression, TempyTable should remain a Table Tag
        self.assertIsInstance(table, Table)

    def test_skeleton_creation(self):
        table = TempyTable(rows=15, cols=10)
        self.assertTrue(table.body)
        # Check table sizes
        self.assertEqual(len(table.body), 15)
        self.assertEqual(len(table.body[0]), 10)

    def test_caption(self):
        table = TempyTable(caption='Test Table')
        self.assertTrue('Test Table' in table.caption)

    def test_init_from_data(self):
        table = TempyTable(data=self.data)
        self.assertEqual(len(table.body), 15)
        self.assertEqual(len(table.body[0]), 10)
        self.verify_content(table)

    def test_populate(self):
        # test no_resize
        table = TempyTable().populate(self.data)
        # Check table sizes
        self.assertEqual(len(table.body), 15)
        self.assertEqual(len(table.body[0]), 10)

        # test add row
        new_data = copy(self.data)
        new_data.append(list(range(1, 11)))
        table.populate(new_data)
        self.assertEqual(len(table.body), 16)

        # test raise with no resize
        new_data[0].append('test')
        with self.assertRaises(WidgetDataError):
            table.populate(new_data)

        # test resize
        table.populate(new_data, resize_x=True)
        self.assertEqual(len(table.body), 16)
        self.assertEqual(len(table.body[0]), 11)
        self.assertEqual(len(table.body[1]), 11)
        self.assertTrue('test' in table.body[0][10])

        # test not force
        for row in new_data:
            try:
                row[10] = 'test1'
            except:
                row.append('test1')
        table.populate(new_data, force=False)
        self.assertEqual(len(table.body), 16)
        self.assertEqual(len(table.body[0]), 11)
        self.assertEqual(len(table.body[1]), 11)
        self.assertFalse('test1' in table.body[0][10])
        self.assertTrue('test1' in table.body[1][10])

        # test force
        table.populate(new_data, force=True)
        self.assertTrue('test1' in table.body[0][10])

        # test non normalize:
        new_data[3].append('test2')
        table.populate(new_data, normalize=False, resize_x=True)
        self.assertTrue('test2' in table.body[3][11])
        with self.assertRaises(IndexError):
            table.body[0][11]

    def test_pop_row(self):
        table = TempyTable(data=self.data)

        # test pop last
        r = table.pop_row()
        self.assertEqual(r, self.data[-1])

        # test pop get tags
        r = table.pop_row(tags=True)
        test_row = Tr()(Td()(c) for c in self.data[-2])
        for cell, t_cell in zip(r, test_row):
            self.assertEqual(cell, t_cell)

        # test pop by index
        r = table.pop_row(0)
        self.assertEqual(r, self.data[0])

    def test_pop_cell(self):
        table = TempyTable(data=self.data)

        # test pop last
        r = table.pop_cell()
        self.assertEqual(r, self.data[-1][-1])

        # test pop get tags
        r = table.pop_cell(tags=True)
        test_cell = Td()(self.data[-2][-1])
        self.assertEqual(r, test_cell)

        # test pop by index row
        r = table.pop_cell(0)
        self.assertEqual(r, self.data[0][-1])

        # test pop by index row andcol
        r = table.pop_cell(0, 0)
        self.assertEqual(r, self.data[0][0])


class TestTempyList(unittest.TestCase):

    def test_create_empty(self):
        li = TempyList()
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 0)

        li = TempyList(Ol)
        self.assertIsInstance(li, Ol)
        self.assertEqual(len(li), 0)

        li = TempyList('Ol')
        self.assertIsInstance(li, Ol)
        self.assertEqual(len(li), 0)

    def test_populate_empty(self):
        li = TempyList()
        li.populate([1, 2, 3])
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)

    def test_create_full(self):
        li = TempyList(struct=[1, 2, 3])
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)
        self.assertTrue(1 in li[0])

        li = TempyList(struct={1, 2, 3})
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)

        li = TempyList(struct={1: None, 2: None, 3: None, '_typ': Ol})
        self.assertIsInstance(li, Ol)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)

    def test_populate_recursive(self):
        li = TempyList()
        li.populate({1: None, 2: ['a', 'b', 'c'], 3: {'test': [1, 2, 3]}})
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)
        self.assertIsInstance(li[1][1], Ul)
        self.assertEqual(len(li[1][1]), 3)
        self.assertIsInstance(li[1][1][0], Li)
        self.assertTrue('a' in li[1][1][0])


if __name__ == '__main__':
    unittest.main()
