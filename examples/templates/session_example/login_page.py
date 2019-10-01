# -*- coding: utf-8 -*-

from tempy.tags import *

def get_page(messages = []):
    divs = [
        Div()(
            'User login'
            ), 
        Div()(
            Form(method = 'POST', action = '/user_page')(
                Div()(
                    Input(type = "text", name = 'username', placeholder = 'Username'),
                ),
                Div()(
                    Input(type = "password", name = 'password', placeholder = 'Password'),
                ),
                Div()(
                    Input(type = "submit")(),
                )
                
            )
        )
    ]
    for message in messages: 
        message_div = [Div()(
            message
        )]
        divs = message_div + divs

    page = Html()(
        Head()(
            Title()(
                'Tempy - Login'
                )
            ),
        body=Body()(
            *divs
        )
    )
    return page
