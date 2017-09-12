# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div, A, Comment, Title


class TestSingleTags(unittest.TestCase):

    def setUp(self):
        self.page = Div()

    def test_fill_a(self):
        a = A(href='www.test.com')
        expected = '<a href="www.test.com">www.test.com</a>'
        self.assertEqual(a.render(), expected)

    def test_comment(self):
        comment_string = 'Test comment'
        c = Comment(comment_string)
        self.assertTrue(comment_string in c.render())

    def test_title(self):
        title_string = 'Test title'
        t = Title(title_string)
        self.assertTrue(title_string in t)
        self.assertEqual(t.render(), '<title>%s</title>' % title_string)
