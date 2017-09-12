# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy import TempyView
from tempy.tags import Div, Td, P, Span


class TestSingleTags(unittest.TestCase):

    def setUp(self):
        class Test:
            def __init__(self):
                self.foo = 'foo'
                self.bar = 'bar'

            class TestView(TempyView):
                def init(self):
                    self(
                        Div()(self.foo),
                        Div()(self.bar)
                        )

            class Div(TempyView):
                def init(self):
                    self(
                        P()(self.foo),
                        P()(self.bar)
                        )

            class Tr(TempyView):
                def init(self):
                    self(
                        Td()(self.foo),
                        Td()(self.bar)
                        )

            class CustomDOMElement(TempyView):
                def init(self):
                    self(
                        Div()(P()(self.foo)),
                        P()(self.bar)
                        )

        self.test_model = Test

    def test_nameless_view(self):
        class Test:
            def __init__(self):
                self.foo = 'foo'
                self.bar = 'bar'

            class TestView(TempyView):
                def init(self):
                    self(
                        Div()(self.foo),
                        Div()(self.bar)
                        )

        test_instance = Test()
        a = Span()(test_instance)
        self.assertEqual(a.render(), '<span><div>foo</div><div>bar</div></span>')

    def test_container_view(self):
        test_instance = self.test_model()
        a = Div()(test_instance)
        self.assertEqual(a.render(), '<div><p>foo</p><p>bar</p></div>')

        b = Span()(Div()(test_instance))
        self.assertEqual(b.render(), '<span><div><p>foo</p><p>bar</p></div></span>')

    def test_root_view(self):
        class CustomDOMElement(Div):
            pass
        test_instance = self.test_model()
        a = CustomDOMElement()(test_instance)
        self.assertEqual(a.render(), '<div><div><p>foo</p></div><p>bar</p></div>')
