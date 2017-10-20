# -*- coding: utf-8 -*-
from flask import url_for
from tempy import Html, Head, Title, Body, P, Img, Br

page = Html()(
    Head()(
        Title()(
            'Tempy - Static files'
        )
    ),
    body=Body()(
            P()("Here's a static picture of a cat!"),
            Img(src='./static/cat.jpg'),
            Br(),
            P()("Here's a static picture of the same cat, but found using flask's url_for, WHOAH!!"),
            Img(src=url_for('static', filename='cat.jpg'))
        )
    )
