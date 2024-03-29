# -*- coding: utf-8 -*-
from tempy.tags import *
from tempy.elements import *
from tempy.content import Content
character = Div(klass='chr')(
        B()(Content('name')),
        P()('height:', Content('height')),
        P()('mass:', Content('mass')),
        P()('hair_color:', Content('hair_color')),
        P()('skin_color:', Content('skin_color')),
        P()('eye_color:', Content('eye_color')),
        P()('birth_year:', Content('birth_year')),
        P()('gender:', Content('gender')),
        P()('homeworld:', Content('homeworld')),
        P()('created:', Content('created')),
        P()('edited:', Content('edited')),
        P()('url:', Content('url')),
    )

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
            Content('characters', t_repr=character)
            )
        )
    )
#print(page.render(pretty=True))
