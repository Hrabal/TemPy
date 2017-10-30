# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy import T, Tag
from tempy.tempy import DOMElement


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
