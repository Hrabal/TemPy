# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Page Widget
"""
import tempy.tags as tags


class TempyPage(tags.Html):
    """HTML Page widget.
    Builds an empty html page with some named common tags:
    - Doctype
    - Head - Title - description meta - keywords meta
    - Body
    Those elements are accessible as page attribute:
    >>> TempyPage.head.charset
    >>> TempyPage.body
    >>> TempyPage.head.title
    Provides an API to manage common meta tags directly.
    """
    __tag = tags.Html._Html__tag

    def __init__(self, title=None, charset="UTF-8", doctype=None, **kwargs):
        content = kwargs.pop("content", None)
        keywords = kwargs.pop("keywords", None)
        super().__init__(**kwargs)
        self.set_title(title or "")
        if content:
            self.set_description(content)
        self.set_charset(charset)
        self.set_keywords(keywords or [])
        if doctype:
            self.set_doctype(doctype)

    def init(self):
        self(
            head=tags.Head()(
                title=tags.Title(),
                charset=tags.Meta(),
                description=tags.Meta(name="description"),
                keywords=tags.Meta(name="keywords"),
            ),
            body=tags.Body(),
        )

    def set_doctype(self, doctype):
        """Changes the <meta> charset tag (default charset in init is UTF-8)."""
        self.doctype.type_code = doctype
        return self

    def set_charset(self, charset):
        """Changes the <meta> charset tag (default charset in init is UTF-8)."""
        self.head.charset.attr(charset=charset)
        return self

    def set_description(self, description):
        """Changes the <meta> description tag."""
        self.head.description.attr(content=description)
        return self

    def set_keywords(self, keywords):
        """Changes the <meta> keywords tag."""
        self.head.keywords.attr(content=", ".join(keywords))
        return self

    def set_title(self, title):
        """Changes the <meta> title tag."""
        self.head.title(title)
        return self
