# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
from tempy import Tag, VoidTag


class Html(Tag):
    __tag = 'html'


class Head(Tag):
    __tag = 'head'


class Meta(VoidTag):
    __tag = 'meta'


class Body(Tag):
    __tag = 'body'


class Div(Tag):
    __tag = 'div'


class P(Tag):
    __tag = 'p'


class Address(Tag):
    __tag = 'address'


class Article(Tag):
    __tag = 'article'


class Aside(Tag):
    __tag = 'aside'


class Footer(Tag):
    __tag = 'footer'


class H1(Tag):
    __tag = 'h1'


class H2(Tag):
    __tag = 'h2'


class H3(Tag):
    __tag = 'h3'


class H4(Tag):
    __tag = 'h4'


class H5(Tag):
    __tag = 'h5'


class H6(Tag):
    __tag = 'h6'


class Header(Tag):
    __tag = 'header'


class Hgroup(Tag):
    __tag = 'hgroup'


class Nav(Tag):
    __tag = 'nav'


class Section(Tag):
    __tag = 'section'


class A(Tag):
    _needed = ('href', )
    __tag = 'a'


class Area(VoidTag):
    __tag = 'area'


class Base(VoidTag):
    __tag = 'base'


class Br(VoidTag):
    __tag = 'br'


class Col(VoidTag):
    __tag = 'col'


class Embed(VoidTag):
    __tag = 'embed'


class Hr(VoidTag):
    __tag = 'hr'


class Img(VoidTag):
    __tag = 'img'


class Input(VoidTag):
    __tag = 'input'


class Link(VoidTag):
    __tag = 'link'


class Param(VoidTag):
    __tag = 'param'


class Source(VoidTag):
    __tag = 'source'


class Track(VoidTag):
    __tag = 'track'


class Wbr(VoidTag):
    __tag = 'wbr'
