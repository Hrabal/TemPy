# -*- coding: utf-8 -*-

from tempy.tags import *
from tempy.elements import Css

my_text_list = ['This is Foo.', 'This is Bar.', 'Have you met my friend Baz?']
another_list = ['Lorem ipsum ', 'dolor sit amet, ', 'consectetur adipiscing elit']

div1 = Div(id='myid', klass='someHtmlClass')('dsfsd', Br())
link = A()
new_css = Css({'html': {
    'body': {
        'color': 'red',
        Div: {
            'color': 'green',
            'border': '1px'
        },
        A: {'color': 'orange'}
    }
},
    '#myid': {'color': 'blue'}
})

new_css.replace_element(['#myid'], {'color': 'purple'})

new_css.replace_element(['html', 'body', Div], {
    'color': 'pink',
    'a': {
        'color': 'red'
    }
})

div2 = Div()
div2.css(width='100px', float='left')
div2.css({'height': '100em'})
div2.css({'background-color': 'blue'})

page = Html()(  # add tags inside the one you created calling the parent
    Head()(  # add multiple tags in one call
        Meta(charset='utf-8'),  # add tag attributes using kwargs in tag initialization
        Link(href="my.css", typ="text/css", rel="stylesheet"),
        new_css
    ),
    body=Body()(  # give them a name so you can navigate the DOM with those names
        div1,
        A(href="www.orange.com")
    )
)

# add tags and content later
page[1][0](A(href='www.bar.com'))  # calling the tag
page[1][0].append(Br())  # using the API
page[1][0].append(A(href='www.baz.com'))  # using the API
page[1][0].append(Br())  # using the API
link = A().append_to(page.body[0])  # access the body as if it's a page attribute
page.body(
    # WARNING! Correct ordering with named Tag insertion is ensured with Python >= 3.5 (because kwargs are ordered)
    testDiv=Div())
link.attr(href='www.python.org')('This is a link to Python.')  # Add attributes and content to already placed tags
