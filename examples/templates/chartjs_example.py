# -*- coding: utf-8 -*-

from tempy.tags import *

page = Html()(
    Head()(
        Title()(
            'Tempy - Hello World!'
            ),
        Script(src="https://cdn.jsdelivr.net/npm/chart.js"),        
        ),
    body=Body()(
        H1()(
            'Hello Chart'
            ),
        Div()
        (Canvas(id='myChart')),
        Script(src='static/setup_chart.js'),
        Script(src='static/render_chart.js')
       )
    )
