# -*- coding: utf-8 -*-
from tempy.tags import *

words = ["These", "are", "all", "in", "seperate", "divs!",]

page = Html()(
    Head()(
        Title()(
            'Tempy - Render List'
            )
        ),
    body=Body()(
        'From unpacking a list: ', *[Div()(w) for w in words],
        'From the same list: ', [Div()(w) for w in words],
        'From and iterator: ', (Div()(w) for w in words),
        'I feel fancy, I use map: ', list(map(lambda x: Div()(x), words)),
    )
)
