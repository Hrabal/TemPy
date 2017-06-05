# -*- coding: utf-8 -*-
from pprint import pprint
from tempy.tags import *

divs = [Div(id=div, klass='inner') for div in range(10)]
my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']

page = Html()(
    Head()(
        Meta(charset='utf-8'),
        Meta(hey='ho')
        ),
    Body()(
        divs,
        A(href='www.this.com'),
        (P(style={'color': '#' + str(p) * 6})(p) for p in range(5)),
        Div()(
            (P()(my_text_list[i]) for i in range(3))
            )
        )
    )

pprint(page.render())
