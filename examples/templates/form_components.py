# -*- coding: utf-8 -*-

from tempy.tags import *

page = Html()(
    Head()(
        Title()(
            'Tempy - Simple Form!'
        )
    ),
    Body()(
        Form()(
            Fieldset()(
                Legend()('Simple Form Components'),
                P()(
                    Label()('Title'),
                    Label()(Input().attr(type='radio', name='title', value='mr'), "Mr"),
                    Label()(Input().attr(type='radio', name='title', value='mr'), "Mrs"),
                    Label()(Input().attr(type='radio', name='title', value='mr'), "Miss")
                ),
                P()(
                    Label()('First name'),
                    Input().attr(type='text', placeholder='First name'),
                ),
                P()(
                    Label()('Last name'),
                    Input().attr(type='text', placeholder='Last name'),
                ),
                P()(
                    Label()('Email'),
                    Input().attr(type='email', placeholder='Email'),
                ),
                P()(
                    Label()('Phone number'),
                    Input('required').attr(type='tel', pattern="\d{3}[\-]\d{3}[\-]\d{4}", placeholder='123-123-1234'),
                ),
                P()(
                    Label()('Password'),
                    Input('required').attr(type='password', placeholder='Password'),
                ),
                P()(
                    Label()('Confirm your password'),
                    Input('required').attr(type='password', placeholder='Password'),
                ),
                P()(
                    Label()('Age'),
                    Input('required').attr(type='range', min=18, max=130),
                ),
                P()(
                    Label()('Country'),
                    Select()(
                        Option().attr(value='1')('Canada'),
                        Option().attr(value='2', selected=True)('France'),
                        Option().attr(value='3')('Germany'),
                        Option().attr(value='4')('Italy'),
                        Option().attr(value='5')('Japan'),
                        Option().attr(value='6')('Russia'),
                        Option().attr(value='7')('United Kingdom')),
                ),
                P()(
                    Label()(
                        Input('required').attr(type="checkbox"),
                        'I agree to the terms and conditions'
                    )
                ),
                Button()('Submit')
            )

        )
    ),

)
