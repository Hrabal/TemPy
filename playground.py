# -*- coding: utf-8 -*-

from tempy.tags import Html, Head, Body, Link

page = Html()(Head(), body=Body())

print(page.render())
page[0](style=Link())
print(page[0].style)
print(page.render())
page.body.after('After the body')
print(page.render())
page.body.before('Before body')
print(page.render())