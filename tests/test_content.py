# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from copy import copy
from collections import Counter
from tempy.tags import Div, P
from tempy.tempy import Content
from tempy.exceptions import ContentError


class TestTag(unittest.TestCase):

    def setUp(self):
        self.test_contents = {'test1': 1, 'test2': {'test21': [1, 2, 3], 'test22': None, 'test23': 'test_string'}}

    def test_init(self):
        with self.assertRaises(ContentError):
            Content()

        cont = Content(name='test')
        self.assertEqual(cont._name, 'test')

        cont = Content(content='test')
        self.assertEqual(list(cont.content), ['test', ])

        cont = Content(content=['test'])
        self.assertEqual(list(cont.content), ['test', ])

        cont = Content(content=('test'))
        self.assertEqual(list(cont.content), ['test', ])

        c = (i for i in (1, 2, 3))
        cont = Content(content=c)
        self.assertEqual(list(cont.content), [1, 2, 3])

        cont = Content(content=('test', ))
        self.assertEqual(list(cont.content), ['test', ])

        cont = Content(content=1)
        self.assertEqual(list(cont.content), [1, ])

        self.assertEqual(cont.length, 1)

        cont = Content(content={'test': 'test'})
        self.assertEqual(list(cont.content), [{'test': 'test'}, ])

        cont = Content(name='test', template=Div())
        self.assertEqual(cont._template, Div())

        with self.assertRaises(ContentError):
            Content(name='test', template='wrong')

    def test_eq(self):
        self.assertEqual(Content(name='test'), Content(name='test'))
        self.assertNotEqual(Content(name='test'), Div)

    def test_render(self):
        d = Div()(Content(name='test1')).inject(self.test_contents)
        self.assertEqual(Counter(d.render()), Counter('<div>1</div>'))

        d = Div()(Content(name='test1'), Content(name='test2')).inject(self.test_contents)
        self.assertEqual(Counter(d.render()), Counter('<div>11 2 3 test_string</div>'))

        d = Div()(Content(name='test1')).inject({'test1': Div()})
        self.assertEqual(Counter(d.render()), Counter('<div><div></div></div>'))

        template = Div()(Content(name='test21'))
        d = Div()(Content(name='test2', template=template)).inject(self.test_contents)
        self.assertEqual(Counter(d.render()), Counter('<div><div>1 2 3</div></div>'))

    def test_content_from_parent(self):
        cont = Content(name='test1')
        d = Div()(cont)
        d.inject(self.test_contents)
        self.assertEqual(list(cont.content), [1, ])

    def test_content_from_granpa(self):
        cont = Content(name='test1')
        p = P()(Div()(cont))
        p.inject(self.test_contents)
        self.assertEqual(list(cont.content), [1, ])

    def test_copy(self):
        cont = Content(name='test', content='test')
        cont2 = copy(cont)
        self.assertEqual(cont, cont2)

    def test_inject_dict(self):
        tag = Div()()
        tag.inject(self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)

    def test_inject_named_dict(self):
        tag = Div()()
        tag.inject(content=self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)

    def test_inject_kwargs(self):
        tag = Div()()
        tag.inject(**self.test_contents)
        self.assertTrue(tag.content_data, self.test_contents)


if __name__ == '__main__':
    unittest.main()
