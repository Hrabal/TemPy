# -*- coding: utf-8 -*-

from tempy.tags import *

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
