# -*- coding: utf-8 -*-

from tempy.tags import Html, Head, Body, Link, Div
from tempy.tempy import Content

page = Html()(Head(), body=Body())

print(page.render())
page[0](style=Link())
print(page[0].style)
print(page.render())
page.body.after('After the body')
print(page.render())
page.body.before('Before body')
print(page.render())
page.body(Content('title'))
page.inject({'title': 'That\'s my title!'})
print(page.render())
page.body.inject({'title': 'That\'s my new title!'})
print(page.render())
page.body(Content('title2'))
print(page.render())
page.body([Div(id=i) for i in range(10)])
print(page.body[1:4])
