# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
All the HTML tags as defined in the W3C reference, in alphabetical order.
"""
from .elements import Tag, VoidTag, Content

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

    def apply_function(self, format_function):
        if not self.childs:
            if 'href' in self.attrs:
                self.attrs['href'] = format_function(self.attrs['href'])
        else:
            gen = ((index, child) for index, child in enumerate(self.childs) if child is not None)
            for (index, child) in gen:
                if isinstance(child, Tag):
                    child.apply_function(format_function)
                elif isinstance(child, Content):
                    child.apply_function(format_function)
                else:
                    self.childs[index] = format_function(self.childs[index])


class Title(Tag):
    __tag = 'title'

    def __init__(self, title=None):
        super().__init__()
        self(title)


tags = {
    VoidTag: ['wbr', 'area', 'base', 'br', 'embed', 'img', 'hr', 'input', 'link', 'meta', 'param', 'source', 'track'],
    Tag: ['abbr', 'acronym', 'address', 'applet', 'article', 'aside', 'audio', 'b', 'basefont', 'bdi', 'bdo', 'big',
          'blockquote', 'body', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'colgroup', 'datalist', 'dd',
          'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'fieldset', 'figcaption', 'figure',
          'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'i',
          'iframe', 'ins', 'kbd', 'keygen', 'label', 'legend', 'li', 'main', 'map', 'mark', 'menu', 'menuitem', 'meter',
          'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'picture', 'pre',
          'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'span', 'strike',
          'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead',
          'time', 'tr', 'tt', 'u', 'ul', 'var', 'video', ]
}


for tag_parent_cls, tags in tags.items():
    for tag in tags:
        tag_cls_name = tag.title()
        # Dynamic class definition
        tag_cls = type(tag_cls_name, (tag_parent_cls, ), {'_%s__tag' % tag_cls_name: tag})
        # We put the new dynamically created class inside locals to make it available from the outside
        locals()[tag_cls_name] = tag_cls

del tag, tag_cls, tag_cls_name, tag_parent_cls, tags
