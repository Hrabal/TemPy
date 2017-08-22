# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body, Div, Content, Br
from tempy_templates.sw_characters import character

page = Html()(
    Head()(
        Title()(
            'Flaskr - SW'
            )
        ),
    body=Body()(
        Div(klass='page')(
            'All the Star Wars characters!',
            Br(),
            Content('characters', template=character)
            )
        )
    )
