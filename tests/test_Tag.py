# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy import Tag, Content
from tempy.tags import Div
from tempy.exceptions import TagError, WrongContentError


class TestTag(unittest.TestCase):

    def test_needed_kargs(self):
        class TestTag(Tag):
           _needed_kwargs = ('test', )

        with self.assertRaises(TagError):
            TestTag()

    def test_index(self):
        father = Div()(Div(), Div())
        d = Div().append_to(father)
        self.assertEqual(d.index, 2)

    def test_stable(self):
        f = Div()
        self.assertTrue(f.stable)
        f(Div())
        self.assertFalse(f.stable)
        f.render()
        self.assertTrue(f.stable)

    def test_rem_attr(self):
        d = Div(test_attr='test')
        d.remove_attr('test_attr')
        self.assertFalse('test_attr' in d.attrs)

    def test_class(self):
        div = Div()
        klass = 'test_class'
        div.add_class(klass)
        self.assertTrue(klass in div.attrs['klass'])
        self.assertTrue(div.has_class(klass))

        # Test adding already present
        div.add_class(klass)
        self.assertTrue(div.has_class(klass))

        div.remove_class(klass)
        self.assertFalse(div.has_class(klass))

        # Test removing not present
        div.remove_class(klass)
        self.assertFalse(div.has_class(klass))

        div.toggle_class(klass)
        self.assertTrue(div.has_class(klass))

        div.toggle_class(klass)
        self.assertFalse(div.has_class(klass))

    def test_css(self):
        div = Div()
        with self.assertRaises(WrongContentError):
            div.css(1, 2, 3)

        div.css({'color': 'blue'})
        self.assertEqual(div.attrs['style'], {'color': 'blue'})

        div.css(**{'color': 'yellow'})
        self.assertEqual(div.attrs['style'], {'color': 'yellow'})

    def test_hide_show(self):
        d = Div()
        d.hide()
        self.assertEqual(d.attrs['style']['display'], 'none')

        d.show()
        self.assertTrue('display' not in d.attrs['style'])

        d.show('inline')
        self.assertEqual(d.attrs['style']['display'], 'inline')

        d.toggle()
        self.assertEqual(d.attrs['style']['display'], 'none')

        d.toggle()
        self.assertTrue('display' not in d.attrs['style'])

    def test_html(self):
        d = Div()(Div())
        self.assertEqual(d.html(), '<div></div>')

    def test_data(self):
        d = Div()
        d.data('test_key', 'test_value')
        self.assertTrue('test_key' in d._data)
        self.assertEqual(d.data('test_key'), 'test_value')
        self.assertEqual(d.data(), {'test_key': 'test_value'})

    def test_text(self):
        d = Div()('test_text')
        self.assertEqual(d.text(), 'test_text')

        d = Div()(Div()('test_text'))
        self.assertEqual(d.text(), 'test_text')

        d = Div()(Div()('test_text'), Div()('test_text2'))
        self.assertEqual(d.text(), 'test_text test_text2')

        d = Div()(Div()('test_text'), Div()('test_text2'), Content(content='test_text3'))
        self.assertEqual(d.text(), 'test_text test_text2 test_text3')

    def test__get_non_tempy_contents(self):
        d = Div()(Div(), 1, Content(name='test'), 'test', False, True, Div())
        self.assertEqual(list(d._get_non_tempy_contents()), [1, 'test', False, True])

if __name__ == '__main__':
    unittest.main()
