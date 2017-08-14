# -*- coding: utf-8 -*-
from tempy import Html, Head, Title, Body

page = Html()(
    Head()(
        Title()(
            'HelloWorld'
            )
        ),
    body=Body()(
        'Hello World'
        )
    )

print(page.render())