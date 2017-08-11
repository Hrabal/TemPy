# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body, Div, Content, Br, B, P

page = Html()(
    Head()(
        Title()(
            'Tempy - Hello World!'
            )
        ),
    body=Body()(
        Div()(
            'Hello World'
            )
        )
    )
