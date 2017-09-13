# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy import TempyREPR
from tempy.tags import Div, Td, P, Span, Table, Tr


class TestSingleTags(unittest.TestCase):

    def setUp(self):
        class Test:
            def __init__(self):
                self.foo = 'foo'
                self.bar = 'bar'
                self.rows = [(1, 2), (3, 4)]

            class Div(TempyREPR):
                def init(self):
                    self(
                        P()(self.foo),
                        P()(self.bar)
                        )

            class Table(TempyREPR):
                def init(self):
                    self(
                        Tr()(
                            Td()(row[0]),
                            Td()(row[1])
                        ) for row in self.rows
                        )

            class CustomDOMElement(TempyREPR):
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

            class TestView(TempyREPR):
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

    def test_tr_complex(self):
        test_instance = self.test_model()
        a = Table()(test_instance)
        self.assertEqual(a.render(), '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')
