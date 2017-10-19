# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body, P, Img

page = Html()(
    Head()(
        Title()(
            'Tempy - Static files'
        )
    ),
    body=Body()(
            P()("Here's a static picture of a cat!"),
            Img(src='./static/cat.jpg')
        )
    )
