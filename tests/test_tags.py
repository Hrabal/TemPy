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

    def test_add(self):
        a = A()
        div = Div()
        result = div + a
        self.assertTrue(a in result)
        self.assertFalse(a in div)
        self.assertEqual(result[0], a)
        self.assertIsNot(div, result)
        same_check = div.clone()(a)
        self.assertEqual(same_check, result)

    def test_iadd(self):
        a = A()
        div = Div()
        div += a
        self.assertTrue(a in div)
        self.assertEqual(div[0], a)

    def test_sub(self):
        a = A()
        div = Div()
        div(a)
        result = div - a
        self.assertFalse(a in result)
        self.assertTrue(a in div)
        self.assertIsNot(div, result)

    def test_isub(self):
        a = A()
        div = Div()
        div(a)
        div -= a
        self.assertFalse(a in div)
        with self.assertRaises(ValueError):
            div -= P()

    def test_mul(self):
        div = Div()
        result = div * 5
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertTrue(div in result)
        self.assertFalse(div.uuid in [tag.uuid for tag in result])
        with self.assertRaises(TypeError):
            result = div * 'string'
        with self.assertRaises(ValueError):
            result = div * -1
        result = div * 0
        self.assertFalse(result)
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    def test_imul(self):
        a = A()
        div = Div()
        div(P(), a, P())
        self.assertEqual(len(div), 3)
        a *= 2
        self.assertTrue(a in div)
        self.assertEqual(len(div), 4)
        self.assertIsInstance(div[2], A)

    def test_imul_zero(self):
        a = A()
        div = Div()
        div(P(), a, P())
        self.assertEqual(len(div), 3)
        a *= 0
        self.assertEqual(len(div), 2)
        self.assertIsInstance(div[1], P)

    def test_getattr(self):
        div = Div(klass='test')
        self.page(test=div)
        test_div = self.page.test
        self.assertEqual(div, test_div)
        test_string = 'test_sting'
        self.page(test2=test_string)
        test_cont = self.page.test2
        self.assertEqual(test_string, test_cont)


if __name__ == '__main__':
    unittest.main()
