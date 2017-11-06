# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
All the HTML tags as defined in the W3C reference, in alphabetical order.
"""
from .elements import Tag, VoidTag

DOCTYPES = {
    'html': 'HTML',
    'html_strict': 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"',
    'html_transitional': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"',
    'html_frameset': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"',
    'xhtml_strict': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"',
    'xhtml_transitional': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"',
    'xhtml_frameset': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"',
    'xhtml_1_1_dtd': 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN"  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"',
    'xhtml_basic_1_1': 'html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd"',
}


class Comment(VoidTag):
    __tag = ''
    _template = '<!-- %s -->'

    def __init__(self, comment_text):
        self._comment = comment_text
        super().__init__()

    def render(self, *args, **kwargs):
        return self._template % self._comment

    def to_code(self, pretty=False):
        return 'Comment("%s")' % self._comment


class Doctype(VoidTag):
    """Doctype is a special tag that needs special rendering.
    It is mandatory to provide a doctype code that will be tranlated into valid HTML doctype coding.
    Avaiable doctype codes: html, html_strict, html_transitional, html_frameset, xhtml_strict, xhtml_transitional,
    xhtml_frameset, xhtml_1_1_dtd, xhtml_basic_1_1
    """
    __tag = '!DOCTYPE'
    _template = '<{tag}{type}>'

    def __init__(self, doctype):
        self.type_code = doctype
        super().__init__()

    def render(self, *args, **kwargs):
        pretty = kwargs.pop('pretty', False)
        return '<!DOCTYPE %s>%s' % (DOCTYPES[self.type_code], '\n' if pretty else '')

    def to_code(self, pretty=False):
        return 'Doctype("%s")' % self.type_code


class Html(Tag):
    """Html tag have a custom render method for it needs to output the Doctype tag outside the main page tree.
    Every Html object is associated with a Doctype object (default doctype code: 'html').
    """
    __tag = 'html'

    def __init__(self, *args, **kwargs):
        # Setting a default doctype: 'html'
        doctype = kwargs.pop('doctype', 'html')
        super().__init__(**kwargs)
        self.doctype = Doctype(doctype)

    def render(self, *args, **kwargs):
        """Override so each html page served have a doctype"""
        return self.doctype.render() + super().render(*args, **kwargs)


class A(Tag):
    __tag = 'a'

    def render(self, *args, **kwargs):
        """Override of the rendering so that if the link have no text in it, the href is used inside the <a> tag"""
        if not self.childs and 'href' in self.attrs:
            return self.clone()(self.attrs['href']).render(*args, **kwargs)
        return super().render(*args, **kwargs)


class Title(Tag):
    __tag = 'title'

    def __init__(self, title=None):
        super().__init__()
        self(title)


class Abbr(Tag):
    __tag = 'abbr'


class Acronym(Tag):
    __tag = 'acronym'


class Address(Tag):
    __tag = 'address'


class Applet(Tag):
    __tag = 'applet'


class Area(VoidTag):
    __tag = 'area'


class Article(Tag):
    __tag = 'article'


class Aside(Tag):
    __tag = 'aside'


class Audio(Tag):
    __tag = 'audio'


class B(Tag):
    __tag = 'b'


class Base(VoidTag):
    __tag = 'base'


class Basefont(Tag):
    __tag = 'basefont'


class Bdi(Tag):
    __tag = 'bdi'


class Bdo(Tag):
    __tag = 'bdo'


class Big(Tag):
    __tag = 'big'


class Blockquote(Tag):
    __tag = 'blockquote'


class Body(Tag):
    __tag = 'body'


class Br(VoidTag):
    __tag = 'br'


class Button(Tag):
    __tag = 'button'


class Canvas(Tag):
    __tag = 'canvas'


class Caption(Tag):
    __tag = 'caption'


class Center(Tag):
    __tag = 'center'


class Cite(Tag):
    __tag = 'cite'


class Code(Tag):
    __tag = 'code'


class Col(VoidTag):
    __tag = 'col'


class Colgroup(Tag):
    __tag = 'colgroup'


class Datalist(Tag):
    __tag = 'datalist'


class Dd(Tag):
    __tag = 'dd'


class Del(Tag):
    __tag = 'del'


class Details(Tag):
    __tag = 'details'


class Dfn(Tag):
    __tag = 'dfn'


class Dialog(Tag):
    __tag = 'dialog'


class Dir(Tag):
    __tag = 'dir'


class Div(Tag):
    __tag = 'div'


class Dl(Tag):
    __tag = 'dl'


class Dt(Tag):
    __tag = 'dt'


class Em(Tag):
    __tag = 'em'


class Embed(VoidTag):
    __tag = 'embed'


class Fieldset(Tag):
    __tag = 'fieldset'


class Figcaption(Tag):
    __tag = 'figcaption'


class Figure(Tag):
    __tag = 'figure'


class Font(Tag):
    __tag = 'font'


class Footer(Tag):
    __tag = 'footer'


class Form(Tag):
    __tag = 'form'


class Frame(Tag):
    __tag = 'frame'


class Frameset(Tag):
    __tag = 'frameset'


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


class Head(Tag):
    __tag = 'head'


class Header(Tag):
    __tag = 'header'


class Hr(VoidTag):
    __tag = 'hr'


class I(Tag):
    __tag = 'i'


class Iframe(Tag):
    __tag = 'iframe'


class Img(VoidTag):
    __tag = 'img'


class Input(VoidTag):
    __tag = 'input'


class Ins(Tag):
    __tag = 'ins'


class Kbd(Tag):
    __tag = 'kbd'


class Keygen(Tag):
    __tag = 'keygen'


class Label(Tag):
    __tag = 'label'


class Legend(Tag):
    __tag = 'legend'


class Li(Tag):
    __tag = 'li'


class Link(VoidTag):
    __tag = 'link'


class Main(Tag):
    __tag = 'main'


class Map(Tag):
    __tag = 'map'


class Mark(Tag):
    __tag = 'mark'


class Menu(Tag):
    __tag = 'menu'


class Menuitem(Tag):
    __tag = 'menuitem'


class Meta(VoidTag):
    __tag = 'meta'


class Meter(Tag):
    __tag = 'meter'


class Nav(Tag):
    __tag = 'nav'


class Noframes(Tag):
    __tag = 'noframes'


class Noscript(Tag):
    __tag = 'noscript'


class Object(Tag):
    __tag = 'object'


class Ol(Tag):
    __tag = 'ol'


class Optgroup(Tag):
    __tag = 'optgroup'


class Option(Tag):
    __tag = 'option'


class Output(Tag):
    __tag = 'output'


class P(Tag):
    __tag = 'p'


class Param(VoidTag):
    __tag = 'param'


class Picture(Tag):
    __tag = 'picture'


class Pre(Tag):
    __tag = 'pre'


class Progress(Tag):
    __tag = 'progress'


class Q(Tag):
    __tag = 'q'


class Rp(Tag):
    __tag = 'rp'


class Rt(Tag):
    __tag = 'rt'


class Ruby(Tag):
    __tag = 'ruby'


class S(Tag):
    __tag = 's'


class Samp(Tag):
    __tag = 'samp'


class Script(Tag):
    __tag = 'script'


class Section(Tag):
    __tag = 'section'


class Select(Tag):
    __tag = 'select'


class Small(Tag):
    __tag = 'small'


class Source(VoidTag):
    __tag = 'source'


class Span(Tag):
    __tag = 'span'


class Strike(Tag):
    __tag = 'strike'


class Strong(Tag):
    __tag = 'strong'


class Style(Tag):
    __tag = 'style'


class Sub(Tag):
    __tag = 'sub'


class Summary(Tag):
    __tag = 'summary'


class Sup(Tag):
    __tag = 'sup'


class Table(Tag):
    __tag = 'table'


class Tbody(Tag):
    __tag = 'tbody'


class Td(Tag):
    __tag = 'td'


class Textarea(Tag):
    __tag = 'textarea'


class Tfoot(Tag):
    __tag = 'tfoot'


class Th(Tag):
    __tag = 'th'


class Thead(Tag):
    __tag = 'thead'


class Time(Tag):
    __tag = 'time'


class Tr(Tag):
    __tag = 'tr'


class Track(VoidTag):
    __tag = 'track'


class Tt(Tag):
    __tag = 'tt'


class U(Tag):
    __tag = 'u'


class Ul(Tag):
    __tag = 'ul'


class Var(Tag):
    __tag = 'var'


class Video(Tag):
    __tag = 'video'


class Wbr(VoidTag):
    __tag = 'wbr'
