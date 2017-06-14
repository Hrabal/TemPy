# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body, Div, Content

page = Html()(
    Head()(
        Title()(
            'Flaskr'
            )
        ),
   body=Body()(
        Div(klass='page')(
            Content('message')
            )
        )
    )
