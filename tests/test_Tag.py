# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div, P, Br
from tempy.elements import Tag, Content
from tempy.exceptions import TagError, WrongContentError, WrongArgsError


class TestTag(unittest.TestCase):

    def test_recursive_tag_get(self):
        class TestTag(Div): pass

        t = TestTag()
        with self.assertRaises(AttributeError):
            t._TestTag__tag
        t._Div__tag
        self.assertEqual(t._get__tag(), 'div')

        class TestTag(Tag): pass
        with self.assertRaises(TagError):
            TestTag()._get__tag()

    def test_tag_set_attrs(self):
        d = Div(klass='test_css_class')
        self.assertTrue('klass' in d.attrs)
        self.assertEqual(d.attrs['klass'], set(['test_css_class', ]))

        d.attr(klass='test_2')
        self.assertEqual(d.attrs['klass'], set(['test_css_class', 'test_2']))

    def test_tag_attrs(self):
        d = Div(id='test_css_id')
        self.assertTrue('id' in d.attrs)
        self.assertEqual(d.attrs['id'], 'test_css_id')

        d.attr(id='test2')
        self.assertEqual(d.attrs['id'], 'test2')

    def test_mapping_tag_attrs(self):
        d = Div(style={'test': 'test_css'})
        self.assertTrue('style' in d.attrs)
        self.assertEqual(d.attrs['style'], {'test': 'test_css'})

        d.attr(style={'test2': 'test_css_2'})
        self.assertEqual(d.attrs['style'], {'test': 'test_css', 'test2': 'test_css_2'})

    def test_tag_bool_attrs(self):
        d = Div(test_boolean=bool)
        self.assertTrue('test_boolean' in d.attrs)
        self.assertEqual(d.attrs['test_boolean'], bool)
        self.assertEqual(d.render(), '<div test_boolean></div>')

    def test_parent(self):
        d = Div()
        p = P().append_to(d)
        self.assertEqual(p.parent, d)

    def test_void_tag_insertion(self):
        with self.assertRaises(TagError):
            d = Br()(Div(id='test_void_tag_insertion'))

        br = Br()
        with self.assertRaises(TagError):
            p = Div().append_to(br)

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

        with self.assertRaises(WrongContentError):
            div.css()

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
        d.data(test_key='test_value')
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

    def test_id_api(self):
        x = Div()
        x.set_id('cssId')
        self.assertTrue(x.is_id('cssId'))
        self.assertEqual(x.id(), 'cssId')
        
        x.set_id('anotherCssId')
        self.assertTrue(x.is_id('anotherCssId'))
        self.assertEqual(x.id(), 'anotherCssId')
