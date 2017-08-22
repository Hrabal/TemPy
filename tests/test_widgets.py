# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from copy import copy

from tempy.widgets import TempyTable
from tempy.tags import Table

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


if __name__ == '__main__':
    unittest.main()
