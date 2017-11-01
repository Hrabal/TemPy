# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest

from tempy.tags import Div, A, P, Html, Head, Body
from tempy.tempy import DOMElement, DOMGroup
from tempy.elements import Tag, TagAttrs
from tempy.exceptions import WrongContentError, TagError


class TestDOMelement(unittest.TestCase):

    def setUp(self):
        self.page = Html()

    def is_tag(self, tag):
        """a tag should be instance of Tag and DOMElement, and should have a TagAttrs attribute)"""
        self.assertIsInstance(tag, Tag)
        self.assertIsInstance(tag, DOMElement)
        self.assertIsInstance(tag.attrs, TagAttrs)

    def check_head_body(self, head, body):
        self.is_tag(head)
        self.is_tag(body)
        self.assertEqual(len(self.page.childs), 2)
        self.assertEqual(self.page.length, 2)
        self.assertEqual(self.page.childs[0], head)
        self.assertEqual(self.page.childs[1], body)
        self.assertEqual(self.page.first(), head)
        self.assertEqual(self.page.last(), body)

    def test_render_raise(self):
        with self.assertRaises(NotImplementedError):
            DOMElement().render()

    def test_create_instantiation(self):
        self.is_tag(self.page)

    def test_create_call_singletag(self):
        head = Head()
        self.page(head)
        self.is_tag(head)
        self.assertEqual(len(self.page.childs), 1)
        self.assertEqual(self.page.length, 1)
        self.assertEqual(self.page.childs[0], head)
        self.assertEqual(self.page.first(), head)
        self.assertEqual(self.page.last(), head)

    def test_own_index(self):
        d = Div()
        p = Div()(d)
        self.assertEqual(d._own_index, 0)
        self.assertEqual(p._own_index, -1)

    def test_create_call_multitag(self):
        head = Head()
        body = Body()
        self.page(head, body)
        self.check_head_body(head, body)

    def test_create_call_list(self):
        l = [Head(), Body()]
        self.page(l)
        self.check_head_body(*l)

    def test_create_call_tuple(self):
        t = (Head(), Body())
        self.page(t)
        self.check_head_body(*t)

    def test_create_call_generator(self):
        g = (t for t in [Head(), Body()])
        self.page(g)
        head, body = self.page.childs
        self.check_head_body(head, body)

    def test_clone(self):
        new = self.page.clone()
        self.assertEqual(new, self.page)

    def test_after(self):
        new1 = Div().append_to(self.page)
        new2 = Div()
        new1.after(new2)
        self.assertEqual(new1._own_index, new2._own_index-1)

    def test_before(self):
        new1 = Div().append_to(self.page)
        new2 = Div()
        new1.before(new2)
        self.assertEqual(new1._own_index, new2._own_index+1)

    def test_prepend(self):
        self.page(Div(), Div())
        new2 = Div()
        self.page.prepend(new2)
        self.assertEqual(new2._own_index, 0)

    def test_prepend_to(self):
        self.page(Div(), Div())
        new2 = Div().prepend_to(self.page)
        self.assertEqual(new2._own_index, 0)

    def test_append(self):
        self.page(Div(), Div())
        new2 = Div()
        self.page.append(new2)
        self.assertEqual(new2._own_index, 2)

    def test__insert_negative_index(self):
        d = Div()
        child = Div()
        d._insert(DOMGroup(None, child), idx=-1)
        self.assertEqual(child._own_index, 0)

    def test_append_to(self):
        self.page(Div(), Div())
        new2 = Div().append_to(self.page)
        self.assertEqual(new2._own_index, 2)

    def test_wrap(self):
        container = Div()
        new = A().wrap(container)
        self.assertTrue(new in container)
        with self.assertRaises(TagError):
            A().wrap(Div()(P()))
        container = Div()
        to_wrap = Div()
        outermost = Div()
        outermost(to_wrap)
        to_wrap.wrap(container)
        self.assertTrue(to_wrap in container)
        self.assertTrue(container in outermost)

    def test_replace_with(self):
        old = Div().append_to(self.page)
        old.replace_with(A())
        self.assertTrue(isinstance(self.page[0], A))

    def test_remove(self):
        new = Div().append_to(self.page)
        new.remove()
        self.assertTrue(new not in self.page)

    def test_move(self):
        new = Div().append_to(self.page)
        self.assertTrue(new in self.page)
        new_container = Div()
        new.move(new_container)
        self.assertTrue(new not in self.page and new in new_container)
        new = Div().append_to(self.page)
        new_container = Div()
        new.move(new_container, name='test')
        self.assertTrue(new not in self.page and new in new_container)
        self.assertEqual(new_container.test, new)

    def test_pop(self):
        new = Div().append_to(self.page)
        self.page.pop(0)
        self.assertTrue(new not in self.page)
        new2 = Div().append_to(self.page)
        self.page.pop()
        self.assertTrue(new2 not in self.page)
        new3 = Div()
        self.page(child_foo=new3)
        self.page.pop('child_foo')
        self.assertTrue(new3 not in self.page)
        new4, new5 = Div(), Div()
        self.page(child_foo_1=new4)
        self.page(child_foo_2=new4)
        self.page.pop(['child_foo_1', 'child_foo_2'])
        self.assertTrue(new4 not in self.page and new5 not in self.page)

    def test_empty(self):
        new = Div().append_to(self.page)
        self.page.empty()
        self.assertTrue(new not in self.page)

    def test_next_magic(self):
        div = Div()(A(), P(), Div())
        test = next(div)
        self.assertTrue(isinstance(test, A))

    def test_reverse(self):
        div = Div()(A(), Div(), P())
        test = next(reversed(div))
        self.assertTrue(isinstance(test, P))

    def test_contents(self):
        test = [A(), Div(), P()]
        div = Div()(test)
        self.assertEqual(div.contents(), test)

    def test_children(self):
        test = [A(), Div(), P(), 'test']
        div = Div()(test)
        self.assertEqual(list(div.children()), test[:-1])

    def test_add(self):
        a = A()
        div = Div()
        result = div + a
        self.assertTrue(a in result)
        self.assertFalse(a in div)
        self.assertEqual(result[0], a)
        self.assertIsNot(div, result)
        same_check = div.clone()(a)
        self.assertEqual(same_check, result)

    def test_iadd(self):
        a = A()
        div = Div()
        div += a
        self.assertTrue(a in div)
        self.assertEqual(div[0], a)

    def test_sub(self):
        a = A()
        div = Div()
        div(a)
        result = div - a
        self.assertFalse(a in result)
        self.assertTrue(a in div)
        self.assertIsNot(div, result)
        with self.assertRaises(ValueError):
            _ = div - P()

    def test_isub(self):
        a = A()
        div = Div()
        div(a)
        div -= a
        self.assertFalse(a in div)
        with self.assertRaises(ValueError):
            div -= P()

    def test_mul(self):
        div = Div()
        result = div * 5
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertTrue(div in result)
        self.assertFalse(div.uuid in [tag.uuid for tag in result])
        with self.assertRaises(TypeError):
            result = div * 'string'
        with self.assertRaises(ValueError):
            result = div * -1
        result = div * 0
        self.assertFalse(result)
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    def test_imul(self):
        a = A()
        div = Div()
        div(P(), a, P())
        self.assertEqual(len(div), 3)
        a *= 2
        self.assertTrue(a in div)
        self.assertEqual(len(div), 4)
        self.assertIsInstance(div[2], A)
        b = Div()
        b *= 2
        self.assertEqual(b, [Div(), Div()])

    def test_imul_zero(self):
        a = A()
        div = Div()
        div(P(), a, P())
        self.assertEqual(len(div), 3)
        a *= 0
        self.assertEqual(len(div), 2)
        self.assertIsInstance(div[1], P)

    def test_getattr(self):
        div = Div(klass='test')
        self.page(test=div)
        test_div = self.page.test
        self.assertEqual(div, test_div)
        test_string = 'test_sting'
        self.page(test2=test_string)
        test_cont = self.page.test2
        self.assertEqual(test_string, test_cont)

    def test_hash(self):
        div1 = Div()
        div2 = div1.clone()
        test_dict = {div1: 0}
        test_dict[div2] = 1
        self.assertEqual(len(test_dict), 2)

    def test_equality(self):
        div1 = Div()
        div2 = Div()
        # Empty same-type tags are equal
        self.assertEqual(div1, div2)

        # Non-empty tags are not equal
        div1(Div())
        self.assertNotEqual(div1, div2)

    def test_childs_index(self):
        div = Div()
        a = A()
        div(P(), P(), a)
        self.assertEqual(div[2], a)

    def test_iter_chidls(self):
        d = Div()
        childs = [A(), P(), P(), Div(), 'test', 1]
        d(childs)
        for i, child in enumerate(d):
            self.assertEqual(childs[i], child)

    def test_next_childs(self):
        d = Div()
        childs = [A(), P(), P(), Div(), 'test', 1]
        d(childs)
        self.assertEqual(childs[0], next(d))

    def test_iter_reversed(self):
        d = Div()
        childs = [A(), P(), P(), Div(), 'test', 1]
        d(childs)
        for t_child, child in zip(reversed(childs), reversed(d)):
            self.assertEqual(t_child, child)

    def test_copy(self):
        from copy import copy
        # Empty tag copy generates equal div
        d1 = Div(test='test')()
        d2 = copy(d1)
        self.assertEqual(d1, d2)

        # A copy of a copy is a copy of the original
        d3 = copy(d2)
        self.assertEqual(d1, d3)

        # Non empty tag copy generates different tag but with same structure
        d1(P())
        d3 = copy(d1)
        self.assertNotEqual(d1, d3)
        self.assertEqual(len(d1.childs), len(d3.childs))
        self.assertEqual(d1.childs[0].__class__, d3.childs[0].__class__)

    def test_move_childs(self):
        childs = [A(), P(), 'test', 0]
        d1 = Div()(childs)
        d2 = Div()
        d1.move_childs(d2)
        self.assertFalse(d1.childs)
        self.assertTrue(d2.childs)
        self.assertEqual(childs[0].parent, d2)

    def test_wrap_inner(self):
        d1, p, a = Div(), P(), A()
        d1(a)
        d1.wrap_inner(p)
        self.assertFalse(a in d1)
        self.assertTrue(a in p)
        self.assertTrue(p in d1)

    def test__find_content(self):
        a = Div()
        a.inject(test='test')
        b = Div()
        a(b)
        b._find_content('test')
        c = P()
        c._find_content('test')

    def test_inject(self):
        a = Div()
        a.inject(test='test')
        self.assertEqual(a.content_data['test'], 'test')
        a.inject({'test2': 'test'})
        self.assertEqual(a.content_data['test2'], 'test')
        a.inject({'test3': 'test'}, test4='test')
        self.assertEqual(a.content_data['test3'], 'test')
        self.assertEqual(a.content_data['test4'], 'test')
        with self.assertRaises(WrongContentError):
            a.inject([1, 2, 3])

    def test_attrs(self):
        d = Div()
        d.attrs['klass'] = 'test'
        self.assertTrue(d.has_class('test'))

        d.attrs['style'] = {'color': 'blue'}
        self.assertEqual(d.attrs['style'], {'color': 'blue'})

        d.attrs['style'] = {'test': 'yellow'}
        self.assertEqual(d.attrs['style'], {'color': 'blue', 'test': 'yellow'})

        d.attrs.update(style={'color': 'blue', 'test': '1'})
        self.assertEqual(d.attrs['style'], {'color': 'blue', 'test': '1'})

    def test_next(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        self.assertEqual(d1.next(), d2)

    def test_next_all(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        d3 = Div().append_to(c)
        self.assertEqual(d1.next_all(), [d2, d3])

    def test_prev(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        self.assertEqual(d2.prev(), d1)

    def test_get_parent(self):
        darth_vader = Div()
        luke = Div().append_to(darth_vader)
        self.assertEqual(luke.get_parent(), darth_vader)

    def test_prev_all(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        d3 = Div().append_to(c)
        self.assertEqual(d3.prev_all(), [d1, d2])

    def test_siblings(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        d3 = Div().append_to(c)
        self.assertEqual(d2.siblings(), [d1, d3])

    def test_parent(self):
        c = Div()
        d1 = Div().append_to(c)
        self.assertEqual(d1.parent, c)

    def test_slice(self):
        c = Div()
        d1 = Div().append_to(c)
        d2 = Div().append_to(c)
        d3 = Div().append_to(c)
        self.assertEqual(c.slice(0, 1), [d1, ])
        self.assertEqual(c.slice(0, 2), [d1, d2])
        self.assertEqual(c.slice(0, 3), [d1, d2, d3])
        self.assertEqual(c.slice(), [d1, d2, d3])
        self.assertEqual(c.slice(0, step=2), [d1, d3])

    def test_root(self):
        a = Div()
        b = Div().append_to(a)
        c = Div().append_to(b)
        self.assertEqual(c.root, a)
        self.assertEqual(b.root, a)
        self.assertEqual(a.root, a)

        c = b.pop()
        self.assertEqual(c.root, c)
        self.assertEqual(b.root, a)
        self.assertEqual(a.root, a)

        b(c)
        d = Div()
        a.move_childs(d)
        self.assertEqual(c.root, d)
        self.assertEqual(b.root, d)
        self.assertEqual(a.root, a)

        c(a)
        self.assertEqual(c.root, d)
        self.assertEqual(b.root, d)
        self.assertEqual(a.root, d)

        c.empty()
        self.assertEqual(a.root, a)

    def test_is_root(self):
        a = Div()
        self.assertTrue(a.is_root)

        b = Div().append_to(a)
        self.assertFalse(b.is_root)

        c = Div().append_to(b)
        self.assertFalse(c.is_root)

    def test_bft(self):
        a, b, c, d, e, f = Div(), Div(), Div(), Div(), Div(), Div()
        a(b(d), c(e(f)))
        l = list(a.bft())
        self.assertTrue(l == [a, b, c, d, e, f])

    def test_dft(self):
        a, b, c, d = Div(), Div(), Div(), Div()
        a(b(d), c)
        l = list(a.dfs_preorder())
        self.assertTrue(l == [a, b, d, c])
        l = list(a.dfs_inorder())
        self.assertTrue(l == [d, b, a, c])
        l = list(a.dfs_postorder())
        self.assertTrue(l == [d, b, c, a])

    def test_dft_reverse(self):
        a, b, c, d = Div(), Div(), Div(), Div()
        a(b(d), c)
        l = list(a.dfs_preorder(reverse=True))
        self.assertTrue(l == [a, c, b, d])
        l = list(a.dfs_inorder(reverse=True))
        self.assertTrue(l == [c, a, d, b])
        l = list(a.dfs_postorder(reverse=True))
        self.assertTrue(l == [c, d, b, a])
