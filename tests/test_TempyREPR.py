# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy import TempyREPR, T
from tempy.exceptions import IncompleteREPRError
from tempy.tags import Div, Td, P, Span, Table, Tr, A, Pre
from tempy.places import *


class TestSingleTags(unittest.TestCase):

    def setUp(self):
        class Test:
            def __init__(self):
                self.foo = 'foo'
                self.bar = 'bar'
                self.rows = [(1, 2), (3, 4)]

            class Div(TempyREPR):
                def repr(self):
                    self(
                        P()(self.foo),
                        P()(self.bar)
                        )

            class Table(TempyREPR):
                def repr(self):
                    self(
                        Tr()(
                            Td()(row[0]),
                            Td()(row[1])
                        ) for row in self.rows
                        )

            class CustomDOMElement(TempyREPR):
                def repr(self):
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

            class HtmlREPR(TempyREPR):
                def repr(self):
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

    def test_incomplete(self):
        class Test:
            def __init__(self):
                self.foo = 'foo'
                self.bar = 'bar'

            class HtmlREPR(TempyREPR):
                pass

        with self.assertRaises(IncompleteREPRError):
            a = Span()(Test())
            a.render()

    def test_inside_places(self):
        class Obj:
            foo = 'foo'
            bar = 'bar'

            class TestA(InsideDiv):
                def repr(self):
                    self(self.bar)

            class A(InsideSpan):
                def repr(self):
                    self(self.foo + 'test')

            class Test2(InsideP):
                def repr(self):
                    self(self.bar + 'test')

        inst = Obj()
        self.assertEqual(Span()(A()(inst)).render(), '<span><a>footest</a></span>')
        self.assertEqual(Div()(Div()(inst)).render(), '<div><div>bar</div></div>')
        self.assertEqual(P()(T.CustomTag()(inst)).render(), '<p><customtag>bartest</customtag></p>')

    def test_near_places(self):
        class Obj:
            foo = 'foo'
            bar = 'bar'

            class TestA(NearDiv):
                def repr(self):
                    self(self.bar)

            class TestB(NearSpan):
                def repr(self):
                    self(self.foo + 'test')

        inst = Obj()
        self.assertEqual(Pre()(Span(), A()(inst)).render(), '<pre><span></span><a>footest</a></pre>')
        self.assertEqual(Pre()(T.Custom()(inst),Div()).render(), '<pre><custom>bar</custom><div></div></pre>')

    def test_before_places(self):
        class Obj:
            foo = 'foo'
            bar = 'bar'

            class TestA(BeforeDiv):
                def repr(self):
                    self(self.bar)

            class A(BeforeSpan):
                def repr(self):
                    self(self.foo + 'test')

        inst = Obj()
        self.assertEqual(Pre()(A()(inst), Span()).render(), '<pre><a>footest</a><span></span></pre>')
        self.assertEqual(Pre()(Div()(inst), Div()).render(), '<pre><div>bar</div><div></div></pre>')
 
    def test_after_places(self):
        class Obj:
            foo = 'foo'
            bar = 'bar'

            class TestA(AfterDiv):
                def repr(self):
                    self(self.bar)

            class A(AfterSpan):
                def repr(self):
                    self(self.foo + 'test')

        inst = Obj()
        self.assertEqual(Pre()(Span(), A()(inst)).render(), '<pre><span></span><a>footest</a></pre>')
        self.assertEqual(Pre()(Div(), Div()(inst)).render(), '<pre><div></div><div>bar</div></pre>')
