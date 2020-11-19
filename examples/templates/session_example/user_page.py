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
            Div()(
                'Hello Admin!',
            ),
            Div()(
                "You are currently logged in, so you can access this page! If you log out, you won't be able to any "
                "more. "
            ),
            Div()(
                "And also, if you try and visit ", A(href="/user_login")("the login page"), "you will be redirected "
                                                                                            "here. ",
            ),
            Div()(
                Form(action='user_logout', method='POST')(
                    Input(type='submit', value='Logout')
                )
            )
        )
    )
)
