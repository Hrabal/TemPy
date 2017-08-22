# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div, A


class TestSingleTags(unittest.TestCase):

    def setUp(self):
        self.page = Div()

    def test_fill_a(self):
        a = A(href='www.test.com')
        expected = '<a href="www.test.com">www.test.com</a>'
        self.assertEqual(a.render(), expected)

if __name__ == '__main__':
    unittest.main()
