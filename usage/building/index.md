---
layout: default
title: Building HTML with Tempy
permalink: /usage/building/
---
TemPy object can be created and asssembled in a tree, each TemPy object can be used later inside another TemPy object.

```python
# --- file: base_elements.py
from tempy.tags import Div, Img, Ul, Li, A
from somewhere import links, foot_imgs
# define some common blocks
header = Div(klass='header')(title=Div()('My website'), logo=Img(src='img.png'))
menu = Div(klass='menu')(Ul()((Li()(A(href=link)) for link in links))
footer = Div(klass='coolFooterClass')(Img(src=img) for img in foot_imgs)
```

```python
# --- file: pages.py
from tempy.tags import Html, Head, Body
from base_elements import header, menu, footer

# import the common blocks and use them inside your page
home_page = Html()(Head(), body=Body()(header, menu, content='Hello world.', footer=footer))
content_page = Html()(Head(), body=Body()(header, menu, Content('header'), Content('content'), footer=footer))
```

```python
# --- file: my_controller.py
from tempy.elements import Content
from tempy.tags import Div
from pages import home_page, content_page

@controller_framework_decorator
def my_home_controller(url='/'):
    return home_page.render()

@controller_framework_decorator
def my_content_controller(url='/content'):
    header = Div()('This is my header!')
    content = "Hi, I'm a content"
    return content_page.render(header=header, content=content)
```

Static parts of pages can be created once an then used in different pages. Blocks can be created and imported as normal Python objects.

<aside class="warning">Depending on the web framework you use, TemPy instances can be shared between http requests. Keep in mind that if you modify a TemPy instance used in various pages, this will be modified in every page and in every subsequent request.</aside>
