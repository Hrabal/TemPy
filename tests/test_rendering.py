# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import unittest
from collections import Counter
from tempy.tags import Html, Head, Body, Link, Div, A, P, Meta, Title
from tempy import render_template


class TestRender(unittest.TestCase):

    def test_render_template(self):
        self.assertEqual(render_template('test', start_directory=os.path.dirname(os.path.realpath(__file__))), '<div></div>')

    def test_page(self):
        self.maxDiff = None
        expected = '<!DOCTYPE HTML><html><head><meta charset="utf-8"/><link href="my.css" type="text/css" rel="stylesheet"/><title>test_title</title></head><body><div class="linkBox"><a href="www.foo.com">www.foo.com</a></div><p>This is foo</p><p>This is Bar</p><p>Have you met my friend Baz?</p>Lorem ipsum dolor sit amet, consectetur adipiscing elit</body></html>'
        my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']
        another_list = ['Lorem ipsum ', 'dolor sit amet, ', 'consectetur adipiscing elit']

        page = Html()(  # add tags inside the one you created calling the parent
            Head()(  # add multiple tags in one call
                Meta(charset='utf-8'),  # add tag attributes using kwargs in tag initialization
                Link(href="my.css", typ="text/css", rel="stylesheet"),
                Title('test_title')
            ),
            body=Body()(  # give them a name so you can navigate the DOM with those names
                Div(klass='linkBox')(
                    A(href='www.foo.com')
                ),
                (P()(text) for text in my_text_list),  # tag insertion accepts generators
                another_list  # add text from a list, str.join is used in rendering
            )
        )
        self.assertEqual(Counter(page.render()), Counter(expected))


if __name__ == '__main__':
    unittest.main()
