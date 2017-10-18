# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body, Div, Content, Br, B, P

words = ["These", "are", "all", "in", "seperate", "divs!",]

page = Html()(
    Head()(
        Title()(
            'Tempy - Render List'
            )
        ),
    body=Body()(
            *[Div()(w) for w in words]
        )
    )
