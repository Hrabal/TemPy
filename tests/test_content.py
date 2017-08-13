# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div
from tempy.tempy import DOMElement, Tag, TagAttrs


class TestTag(unittest.TestCase):

    def setUp(self):
        self.test_contents = {'test1': 1, 'test2': {1: [1, 2, 3], 2: None}}

    def is_tag(self, tag):
        self.assertIsInstance(tag, Tag)
        self.assertIsInstance(tag, DOMElement)
        self.assertIsInstance(tag.attrs, TagAttrs)

    def test_inject_dict(self):
        tag = Div()()
        tag.inject(self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)

    def test_inject_named_dict(self):
        tag = Div()()
        tag.inject(content=self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)

    def test_inject_kwargs(self):
        tag = Div()()
        tag.inject(**self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)


if __name__ == '__main__':
    unittest.main()
