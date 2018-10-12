# -*- coding: utf-8 -*-
from tempy.tags import *

examples = {"Hello World":"/hello_world", "Star Wars":"/star_wars",
		"List":"/list", "Static Image":"/static", "Table":"/table", "CSS":"/css"}

container = Div()(
    'content: ', Div()('this is the content')
)

page = Html()(
    Head()(
        Title()(
            'Tempy - Examples'
            )
        ),
    body=Body()(
		*[Div()(A(href=examples.get(k))(k)) for k in examples],
       
    )
)
