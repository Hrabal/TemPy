# -*- coding: utf-8 -*-
from pyquery.tags import *

divs = [Div(id=div, klass='inner') for div in range(10)]

page = Html()(
    Head()(
        Meta(charset='utf-8'),
        Meta(hey='ho')
        ),
    Body()(
        divs,
        A(href='www.this.com'),
        (P() for p in range(5))
        )
    )


my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']
page = Html()(
    Head()(
        Meta(charset='utf-8'),
        Link(href="my.css", typ="text/css", rel="stylesheet")
    ),
    Body()(
        Div(klass='linkBox')(
            A(href='www.foo.bar')
        ),
        (P()(my_text_list[i]) for i in range(3))
    )
).render()

from pprint import pprint
pprint(page)

divs = [Div() for div in range(10)]
ps = (P() for _ in range(10))
container_div = Div()(divs)
print container_div.childs
for i, div in enumerate(container_div):
    div.attr(id='divId'+str(i))
container_div[0].append(ps)
container_div[0][4].attr(id='uniquePid')
print container_div.render()

