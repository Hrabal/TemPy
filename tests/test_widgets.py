# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from copy import copy

from tempy.widgets import TempyTable, TempyList, TempyPage
from tempy.tags import Table, Tr, Td, Dl, Dt, Dd, Ul, Ol, Li, Html, Head, Body, Thead, Tfoot

from tempy.exceptions import WidgetDataError, WidgetError


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
        self.assertFalse(table.body.childs)
        self.assertTrue(table.body)
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

    def test_init_from_data_full(self):
        table = TempyTable(data=self.data, head=True, foot=True)
        self.assertEqual(len(table.body), 13)
        self.assertIsInstance(table.header, Thead)
        self.assertIsInstance(table.footer, Tfoot)

    def test_populate(self):
        table = TempyTable().populate(self.data)
        # Check table sizes
        self.assertEqual(len(table.body), 15)
        self.assertEqual(len(table.body[0]), 10)

        # test add row
        new_data = copy(self.data)
        new_data.append(list(range(1, 11)))
        table.populate(new_data)
        self.assertEqual(len(table.body), 16)

        # test resize
        print('test resize')
        new_data.append(list(range(1, 12)))
        table.populate(new_data)
        self.assertEqual(len(table.body), 17)
        self.assertEqual(len(table.body[0]), 11)
        self.assertEqual(len(table.body[1]), 11)
        self.assertEqual(len(table.body[-1]), 11)

        # test non normalize:
        new_data[3].append('test2')
        table.populate(new_data, normalize=False)
        self.assertTrue('test2' in table.body[3][10])
        self.assertEqual(len(table.body[1]), 10)
        self.assertEqual(len(table.body[3]), 11)
        with self.assertRaises(IndexError):
            table.body[6][11]

        with self.assertRaises(WidgetDataError):
            table.populate(None)

    def test_clear(self):
        table = TempyTable(data=self.data)
        table.clear()

        self.assertTrue(table.body.is_empty)

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

        with self.assertRaises(WidgetError):
            li = TempyList('Wrong')

    def test_populate_empty(self):
        li = TempyList()
        li.populate([1, 2, 3])
        self.assertIsInstance(li, Ul)
        self.assertEqual(len(li), 3)
        self.assertIsInstance(li[0], Li)
        with self.assertRaises(WidgetDataError):
            li.populate('wrong type')
        li = TempyList(typ=Dl)
        li.populate({1: 'one', 2:'two', 34:['three', 'four']})
        self.assertIsInstance(li, Dl)
        self.assertEqual(len(li), 7)
        self.assertIsInstance(li[0], Dt)
        self.assertIsInstance(li[1], Dd)
        self.assertIsInstance(li[6], Dd)
        with self.assertRaises(WidgetDataError):
            li.populate('wrong type')

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


class TestTempyPage(unittest.TestCase):

    def test_create(self):
        page = TempyPage()
        self.assertIsInstance(page, Html)
        self.assertEqual(len(page), 2)
        self.assertIsInstance(page.head, Head)
        self.assertIsInstance(page.body, Body)
        self.assertEqual(len(page.head.title), 0)
        self.assertEqual(page.head.charset.attrs['charset'], 'UTF-8')

    def test_charset(self):
        page = TempyPage()
        self.assertEqual(page.head.charset.attrs['charset'], 'UTF-8')
        page.set_charset('text/html;charset=ISO-8859-1')
        self.assertEqual(page.head.charset.attrs['charset'], 'text/html;charset=ISO-8859-1')

    def test_description(self):
        page = TempyPage()
        page.set_description('test page')
        self.assertEqual(page.head.description.attrs['content'], 'test page')

    def test_keywords(self):
        page = TempyPage()
        kw = ['test', 'foo', 'bar']
        page.set_keywords(kw)
        self.assertEqual(page.head.keywords.attrs['content'], ', '.join(kw))

    def test_doctype(self):
        page = TempyPage()
        page.set_doctype('html_strict')
        charset_string = 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"'
        self.assertTrue(charset_string in page.render())
