# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div, A, P, Html, Head, Body
from tempy.tempy import DOMElement, Tag, TagAttrs


class TestDOMelement(unittest.TestCase):

    def setUp(self):
        self.page = Html()

    def is_tag(self, tag):
        """a tag should be instance of Tag and DOMElement, and should have a TagAttrs attribute)"""
        self.assertIsInstance(tag, Tag)
        self.assertIsInstance(tag, DOMElement)
        self.assertIsInstance(tag.attrs, TagAttrs)

    def check_head_body(self, head, body):
        self.is_tag(head)
        self.is_tag(body)
        self.assertEqual(len(self.page.childs), 2)
        self.assertEqual(self.page.length, 2)
        self.assertEqual(self.page.childs[0], head)
        self.assertEqual(self.page.childs[1], body)
        self.assertEqual(self.page.first(), head)
        self.assertEqual(self.page.last(), body)

    def test_create_instantiation(self):
        self.is_tag(self.page)

    def test_create_call_singletag(self):
        head = Head()
        self.page(head)
        self.is_tag(head)
        self.assertEqual(len(self.page.childs), 1)
        self.assertEqual(self.page.length, 1)
        self.assertEqual(self.page.childs[0], head)
        self.assertEqual(self.page.first(), head)
        self.assertEqual(self.page.last(), head)

    def test_create_call_multitag(self):
        head = Head()
        body = Body()
        self.page(head, body)
        self.check_head_body(head, body)

    def test_create_call_list(self):
        l = [Head(), Body()]
        self.page(l)
        self.check_head_body(*l)

    def test_create_call_tuple(self):
        t = (Head(), Body())
        self.page(t)
        self.check_head_body(*t)

    def test_create_call_generator(self):
        g = (t for t in [Head(), Body()])
        self.page(g)
        head, body = self.page.childs
        self.check_head_body(head, body)

    def test_clone(self):
        new = self.page.clone()
        self.assertEqual(new, self.page)

    def test_after(self):
        new1 = Div().append_to(self.page)
        new2 = Div()
        new1.after(new2)
        self.assertEqual(new1._own_index, new2._own_index-1)

    def test_before(self):
        new1 = Div().append_to(self.page)
        new2 = Div()
        new1.before(new2)
        self.assertEqual(new1._own_index, new2._own_index+1)

    def test_prepend(self):
        self.page(Div(), Div())
        new2 = Div()
        self.page.prepend(new2)
        self.assertEqual(new2._own_index, 0)

    def test_prepend_to(self):
        self.page(Div(), Div())
        new2 = Div().prepend_to(self.page)
        self.assertEqual(new2._own_index, 0)

    def test_append(self):
        self.page(Div(), Div())
        new2 = Div()
        self.page.append(new2)
        self.assertEqual(new2._own_index, 2)

    def test_append_to(self):
        self.page(Div(), Div())
        new2 = Div().append_to(self.page)
        self.assertEqual(new2._own_index, 2)

    def test_wrap(self):
        new = Div().wrap(self.page)
        self.assertTrue(new in self.page)

    def test_replace_with(self):
        old = Div().append_to(self.page)
        old.replace_with(A())
        self.assertTrue(isinstance(self.page[0], A))

    def test_remove(self):
        new = Div().append_to(self.page)
        new.remove()
        self.assertTrue(new not in self.page)

    def test_move(self):
        new = Div().append_to(self.page)
        new_container = Div()
        new.move(new_container)
        self.assertTrue(new not in self.page and new in new_container)

    def test_pop(self):
        new = Div().append_to(self.page)
        self.page.pop(0)
        self.assertTrue(new not in self.page)

    def test_empty(self):
        new = Div().append_to(self.page)
        self.page.empty()
        self.assertTrue(new not in self.page)

    def test_next(self):
        div = Div()(A(), P(), Div())
        test = next(div)
        self.assertTrue(isinstance(test, A))

    def test_reverse(self):
        div = Div()(A(), Div(), P())
        test = next(reversed(div))
        self.assertTrue(isinstance(test, P))


if __name__ == '__main__':
    unittest.main()
