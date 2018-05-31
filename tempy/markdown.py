# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
from mistune import Renderer, Markdown

from .tags import A, P, Strong, Em, Code, Escaped, Pre, Blockquote


class MarkdownRenderer(Renderer):

    def placeholder(self):
        return []

    def paragraph(self, text):
        return [P()(text), ]

    def link(self, link, title, text):
        return [A(href=link, title=title)(text), ]

    def double_emphasis(self, text):
        return [Strong()(text), ]

    def emphasis(self, text):
        return [Em()(text), ]

    def block_code(self, code, lang=None):
        attrs = {}
        if lang:
            attrs['klass'] = 'lang-%s' % lang
        return [Pre()(Code(**attrs)(Escaped(code))), ]

    def block_quote(self, text):
        return [Blockquote(text), ]

markdown_parser = Markdown(renderer=MarkdownRenderer())
