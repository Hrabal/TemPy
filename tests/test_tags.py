# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import *
from tempy.tempy import DOMElement, Tag, TagAttrs


class TestTag(unittest.TestCase):

    def setUp(self):
        self.page = Html()

    def is_tag(self, tag):
        self.assertIsInstance(tag, Tag)
        self.assertIsInstance(tag, DOMElement)
        self.assertIsInstance(tag.attrs, TagAttrs)

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
        self.is_tag(head)
        self.is_tag(body)
        self.assertEqual(len(self.page.childs), 2)
        self.assertEqual(self.page.length, 2)
        print '*'*100
        print self.page.childs
        print '*'*100
        self.assertEqual(self.page.childs[0], head)
        self.assertEqual(self.page.childs[1], body)
        self.assertEqual(self.page.first(), head)
        self.assertEqual(self.page.last(), body)

    def test_create_call_iterable(self):
        divs = [Div() for _ in range(10)]
        self.page.childs[1](divs)
        body = self.page.childs[1]
        self.is_tag(self.page.childs[1][1])
        self.assertEqual(len(self.page.childs), self.page.length)
        self.assertEqual(self.page.length, 2)
        self.assertEqual(len(body.childs), body.length)
        self.assertEqual(body, 10)
        self.assertIsInstance(self.page.childs[0][0], Div)


if __name__ == '__main__':
    unittest.main()
