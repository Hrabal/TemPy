# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import importlib
from mistune import Renderer

from .tempy import Escaped


class TempyMarkdownRenderer(Renderer):
    _tempy_tags = importlib.import_module('.tags', package='tempy')

    def placeholder(self):
        return []

    def text(self, text):
        return [text, ]

    def paragraph(self, text):
        return [self._tempy_tags.P()(text), ]

    def link(self, link, title, text):
        return [self._tempy_tags.A(href=link, title=title)(text), ]

    def double_emphasis(self, text):
        return [self._tempy_tags.Strong()(text), ]

    def emphasis(self, text):
        return [self._tempy_tags.Em()(text), ]

    def block_code(self, code, lang=None):
        attrs = {}
        if lang:
            attrs['klass'] = 'lang-%s' % lang
        return [self._tempy_tags.Pre()(self._tempy_tags.Code(**attrs)(Escaped(code))), ]

    def block_quote(self, text):
        return [self._tempy_tags.Blockquote()(text), ]

    def header(self, text, level, raw=None):
        HeaderTag = getattr(self._tempy_tags, 'H%s' % level, None)
        return [HeaderTag()(text), ]

    def hrule(self):
        return [self._tempy_tags.Hr(), ]

    def list(self, body, ordered=True):
        tag = 'Ul' if not ordered else 'Ol'
        ListTag = getattr(self._tempy_tags, tag, None)
        return [ListTag()(body), ]

    def list_item(self, text):
        return [self._tempy_tags.Li()(text), ]

    def table(self, header, body):
        return [
            self._tempy_tags.Table()(
                self._tempy_tags.Thead()(header),
                self._tempy_tags.Tbody()(body)
            )
        ]

    def table_row(self, content):
        return [self._tempy_tags.Tr()(content), ]

    def table_cell(self, content, **flags):
        tag = 'Th' if flags['header'] else 'Td'
        kwattrs = {}
        align = flags['align']
        if align:
            kwattrs['style'] = "text-align:%s" % align
        CellTag = getattr(self._tempy_tags, tag, None)
        return [CellTag(**kwattrs)(content), ]

    def codespan(self, text):
        return [self._tempy_tags.Code()(text), ]

    def linebreak(self):
        return [self._tempy_tags.Br(), ]

    def strikethrough(self, text):
        return [self._tempy_tags.Del()(text), ]

    def autolink(self, link, is_email=False):
        text = link
        if is_email:
            link = 'mailto:%s' % link
        return [self._tempy_tags.A(href=link)(text), ]

    def image(self, src, title, text):
        kwattrs = {'src': src, 'alt': text}
        if title:
            kwattrs['title'] = title
        return [self._tempy_tags.Img(**kwattrs), ]

    def footnote_ref(self, key, index):
        return [
            self._tempy_tags.Sup(klass="footnote-ref", id="ref-%s" % key)(
                self._tempy_tags.A(href="#fn-%s" % key)(index)
            )
        ]

    def footnote_item(self, key, text):
        return [
            self._tempy_tags.Li(id="fn-%s" % key)(
                text,
                self._tempy_tags.P()(
                    self._tempy_tags.A(href="#fnref-%s" % key)('&#8617;')
                )
            )
        ]

    def footnotes(self, text):
        return [
            self._tempy_tags.Div(klass="footnotes")(
                self._tempy_tags.Hr(),
                self._tempy_tags.Ol()(text)
            )
        ]
