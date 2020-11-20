# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import html
import unittest
from collections import Counter

from tempy import T, Tag, VoidTag
from tempy.tempy import DOMElement
from tempy.tags import Div, A, Br, Doctype, Comment


class TestTag(unittest.TestCase):

    def test_getattr(self):
        # Test T tempt tag factory __getattr__
        custom_tag = T.CustomTag()
        self.assertIsInstance(custom_tag, Tag)
        self.assertIsInstance(custom_tag, DOMElement)
        self.assertEqual(custom_tag._CustomTag__tag, 'customtag')
        self.assertEqual(custom_tag.__class__.__name__, 'CustomTag')

    def test_getitem(self):
        # Test T tempt tag factory __getitem__
        custom_tag = T['CustomTag']()
        self.assertIsInstance(custom_tag, Tag)
        self.assertIsInstance(custom_tag, DOMElement)
        self.assertEqual(custom_tag._CustomTag__tag, 'customtag')
        self.assertEqual(custom_tag.__class__.__name__, 'CustomTag')

    def test_getitem_multiple(self):
        # Test T tempt tag factory __getitem__ with various names
        tags = ['firsttag', 'second_tag', 'third tag', 'Fourth Tag']
        custom_tags = [T[t]() for t in tags]
        for t, t_inst in zip(tags, custom_tags):
            self.assertIsInstance(t_inst, Tag)
            self.assertIsInstance(t_inst, DOMElement)
            self.assertEqual(t_inst._get__tag(), t.lower())
            self.assertEqual(t_inst.__class__.__name__, t)

    def test_render(self):
        # Test T tempt tag factory rendering
        t = T.Test()
        self.assertEqual(t.render(), '<test></test>')

    def test_void(self):
        # Test T tempt tag factory __getattr__
        t = T.Void.Test()
        self.assertIsInstance(t, Tag)
        self.assertIsInstance(t, DOMElement)
        self.assertEqual(t._Test__tag, 'test')
        self.assertEqual(t.__class__.__name__, 'Test')
        self.assertEqual(t.render(), '<test/>')

    def test_void_getitem(self):
        # Test T tempt tag factory rendering
        t = T.Void['Test']()
        self.assertIsInstance(t, Tag)
        self.assertIsInstance(t, DOMElement)
        self.assertEqual(t._Test__tag, 'test')
        self.assertEqual(t.__class__.__name__, 'Test')
        self.assertEqual(t.render(), '<test/>')

    def test_parser_base(self):
        # Test the T parser
        div_string = '<div></div>'
        tempy_elements = T.from_string(div_string)
        self.assertIsInstance(tempy_elements[0], Div)

        a_string = '<a></a>'
        tempy_elements = T.from_string(a_string)
        self.assertIsInstance(tempy_elements[0], A)

        br_string = '<br>'
        tempy_elements = T.from_string(br_string)
        self.assertIsInstance(tempy_elements[0], Br)

        custom_string = '<custom>'
        tempy_elements = T.from_string(custom_string)
        self.assertIsInstance(tempy_elements[0], DOMElement)
        self.assertIsInstance(tempy_elements[0], Tag)

        custom_string = '<custom_void/>'
        tempy_elements = T.from_string(custom_string)
        self.assertIsInstance(tempy_elements[0], VoidTag)
        self.assertIsInstance(tempy_elements[0], DOMElement)
        self.assertIsInstance(tempy_elements[0], Tag)

    def test_parser_multi(self):
        # Tests T parese with multiple non-nested elements
        multi_string = '<a></a><div></div>'
        tempy_elements = T.from_string(multi_string)
        self.assertIsInstance(tempy_elements[0], A)
        self.assertIsInstance(tempy_elements[1], Div)

    def test_parser_nested(self):
        # Tests T parese with multiple nested elements
        html_string = '<div><a></a></div>'
        tempy_elements = T.from_string(html_string)
        self.assertIsInstance(tempy_elements[0], Div)
        self.assertIsInstance(tempy_elements[0][0], A)
        self.assertEqual(tempy_elements[0].render(), html_string)

    def test_parser_attrs(self):
        # Tests parser dealing with tag attributes
        html_string = '<div class="cssClass"></div>'
        temped = T.from_string(html_string)[0]
        self.assertTrue(temped.has_class("cssClass"))

        html_string = '<div class="cssClass" id="cssId"></div>'
        temped = T.from_string(html_string)[0]
        self.assertTrue(temped.is_id("cssId"))

        html_string = '<div custom_attr="foo"></div>'
        temped = T.from_string(html_string)[0]
        self.assertEqual(temped.attrs["custom_attr"], 'foo')

        html_string = '<div custom_bool_attr></div>'
        temped = T.from_string(html_string)[0]
        self.assertIsInstance(temped.attrs["custom_bool_attr"], bool)

    def test_parser_contents(self):
        # Parsed handling of tag contents
        content = "I'm a content"
        html_string = '<div>'+content+'</div>'        
        temped = T.from_string(html_string)[0]
        self.assertEqual(temped.childs[0], content)
        self.assertEqual(temped.text(), content)
        self.assertEqual(temped.html(), html.escape(content))

    def test_dump(self):
        # Test T dumping a Tempy object to a file
        result = """# -*- coding: utf-8 -*-
from tempy import T
from tempy.tags import *
Div(klass="cssClass", bool_attr="True")(A(href=\"\"\"www.foo.bar\"\"\")(\"\"\"non-tempy content\"\"\"), T.CustomTag(numb_attr=9), Br(), Doctype("html"), Comment("test comment"), T.Void.TestVoid())"""
        filename = 'test.py'
        tempy_tree = [Div(klass='cssClass', bool_attr=bool)(A(href='www.foo.bar')('non-tempy content'),
                                                            T.CustomTag(numb_attr=9), Br(), Doctype('html'),
                                                            Comment('test comment'), T.Void.TestVoid()), ]
        T.dump(tempy_tree, filename)
        with open(filename, 'r') as f:
            self.assertEqual(Counter(f.read()), Counter(result))
        os.remove(filename)

        T.dump(tempy_tree, 'test')
        os.remove(filename)

        with self.assertRaises(ValueError):
            T.dump(tempy_tree, 'test.jpg')

        with self.assertRaises(ValueError):
            T.dump(tempy_tree, None)
