# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from tempy import T
from tempy.tags import P


class TestTag(unittest.TestCase):

    def test_markdown_return_empty(self):
        t = ''
        r = T.from_markdown(t)
        self.assertEqual(r, [])
        self.assertIsInstance(r, list)

    def test_markdown_return_P_wrap(self):
        t = 'Lorem ipsum'
        r = T.from_markdown(t)
        self.assertIsInstance(r[0], P)

    def test_heading(self):
        t = """Heading
            ======="""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h1>Heading</h1>')

    def test_sub_heading(self):
        t = """Sub-heading
 -----------"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h2>Sub-heading</h2>')

    def test_h3_heading(self):
        t = """### H3 heading"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h3>H3 heading</h3>')

    def test_line_break(self):
        t = """Text in a paragraph that ends with two spaces  
other text"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>Text in a paragraph that ends with two spaces<br/>other text</p>')

    def test_italic(self):
        t = """*italic*"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><em>italic</em></p>')

    def test_bold(self):
        t = """**bold**"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><strong>bold</strong></p>')

    def test_code_inline(self):
        t = """`monospace`"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><code>monospace</code></p>')

    def test_strikethrough(self):
        t = """~~strikethrough~~"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><del>strikethrough</del></p>')

    def test_link(self):
        t = """A [link](https://hrabal.github.io/TemPy/)."""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>A <a href="https://hrabal.github.io/TemPy/">link</a>.</p>')

    def test_list(self):
        t = """Important list:
 
   * foo
   * bar
   * baz"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Important list:</p><ul><li>foo</li><li>bar</li><li>baz</li></ul>')

    def test_list_numbered(self):
        t = """Important Numbered list:
 
   1. foo
   2. bar
   3. baz"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Important Numbered list:</p><ol><li>foo</li><li>bar</li><li>baz</li></ol>')

    def test_markdown_escape(self):
        t = """&"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>&amp;</p>')
