# -*- coding: utf-8 -*-
from pyquery.tags import *
from pyquery import pyQ
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

print(page.render())
page.childs[1].append(Div(id=42))
print(page.render())
page.childs[1].childs[11].remove()
print(page.render())
page[0][1].remove()
print(page.render())
page[0].pop(0)
print(page.render())

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

for i, div in enumerate(container_div):
    div.attr(id='divId'+str(i))
container_div[0].append(ps)
container_div[0][4].attr(id='uniquePid')
print container_div.render()

from pprint import pprint
pprint(pyQ.__dict__)

print(pyQ(P))
