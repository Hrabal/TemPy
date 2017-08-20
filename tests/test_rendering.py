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


if __name__ == '__main__':
    unittest.main()
