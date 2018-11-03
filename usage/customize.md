---
layout: default
title: Customizing TemPy Tags
permalink: /usage/customize/
---

# Customizing TemPy Tags

## TemPy Tags Factory
```python
from tempy import T
```

### Custom Tags from T

If you need a tag with a custom name the easiest way is to use the `T` object. The T object is a multi-feature object that work as a class factory for custom tags.

```python
from tempy import T
from tempy.elements import Tag

Custom = T.MyCustomTag
# Custom is a class that have all the TemPy features and api
Custom
>>> <class tempy.t.Custom>
issubclass(Custom, Tag)
>>> True

# And will be rendered with the lowercase version of the name with wich you accessed T
# with wich you accessed T
Custom().render()
>>> <mycustomtag></mycustomtag>
```

Accessing an attribute/key of the T object will produce a TemPy Tag (or VoidTag) subclass named after the given attribute/key (in lowercase).

```python
# Create a custom tag with some fixed attributes:
Readonly = T['textarea readonly']
Readonly('This is the text in the textarea').render()
>>> <textarea readonly></textarea readonly>

# Same for void tags using the Void specialized class factory
my_void_tag = T.Void.CustomVoid
my_void_tag().render()
>>> <customvoid/>
```

Classes made with `T` are subclasses of `tempy.tempy.DOMElement` and behave like any other TemPy Tag, they inherit the api and the features of TemPy objects.

### Parse existing HTML using T

`T` can also produce TemPy tags from html strings on the fly. Using the `from_string` method it converts html strings into a list of TemPy trees:

```python
from tempy import T
html_string = """<div>I come from a <i>weird</i> webservice that returns html strings, 
from an old file or from an http request, <b>beware!</b></div>"""
parsed = T.from_string(html_string)
div = parsed[0]
div
>>> <tempy.tags.Div 4340523584. 4 childs.>
div[0]
>>> 'I come from a '
div[1]
>>> <tempy.tags.I 4344205664. Son of Div. 1 childs.>
div[1][0]
>>> 'weird'
```



***


Subclassing Tempy tags
======

It's possible to define custom tags subclassing `tempy.elements.Tag` or `tempy.elements.VoidTag`.
A TemPy Tag subclass:
 * *can* implement a custom `__tag` attribute
 * *can* implement a custom `render` method.
 * *can* implement a custom `__init__` method.

```python
from tempy.elements import Tag

# Making a tag that repeats itself, why? Because!
class Double(Tag):
    __tag = 'custom'
    def render(self, *args, **kwargs):
        return super().render(*args, **kwargs) * 2

Double()('content').render()
>>> <custom>content</custom><custom>content</custom>
```

### A more complex example

For instance if you are using Bootstrap's grid system in your site, you would have to write a lot of code like this:

```python
Div(klass='container')(
    Div(klass='row')(
        Div(klass='col')('Content of the first cell, first row'),
        Div(klass='col')('Content of the second cell, first row')
    ),
    Div(klass='row')(
        Div(klass='col')('Content of the first cell, second row'),
        Div(klass='col')('Content of the second cell, second row')
    ),
)
# ..or maybe this:
Div(klass='container')(
    Div(klass='row')(
        Div(klass='col')(content) for content in row
    ) for row in table_of_contents,
)
```

We can define a `Grid` class that automatically creates the `container->row->col` css class structure:
```python
from tempy.tags import Div


class Grid(Div):
    def __init__(self, rows=0, cols=0):
        super().__init__(klass='container')
        for _ in range(rows):
            row = Div(klass='row')
            for _ in range(cols):
                row(Div(klass='col'))
            self(row)
```

With our new Grid tag class we can make Bootstrap grids without having to make the Div grid everytime:
```python
pictures = ['img1.jpg', 'img2.jpg', 'someImage.gif', 'img3.jpg', 'img4.jpg', 'bestImage.jpg']

articles = some_function_that_returns_a_list_of_articles()

image_grid = Grid(rows=int(len(pictures) / 3), cols=3)
articles_grid = Grid(rows=int(len(articles) / 3), cols=3)

for i, image in enumerate(pictures):
    row = int(i / 3)
    col = i - row * 3
    image_grid[row][col](Img(src=image))

for i, content in enumerate(articles):
    row = int(i / 3)
    col = i - row * 3
    articles_grid[row][col](content)
```

We can go further and make our `Grid` tag more easy to use and let him handle the contents:

```python
from itertools import zip_longest
from tempy.tags import Div, A, Img


class Grid(Div):
    def __init__(self, contents, cols, fillvalue=None):
        super().__init__(klass='container')
        self._fillvalue = fillvalue
        self._cols = cols
        for contents_row in self._group_contents(contents):
            row = Div(klass='row')
            for content in contents_row:
                row(Div(klass='col')(content))
            self(row)

    def _group_contents(self, contents):
        # Group the contents in a list of cols-length lists
        args = [iter(contents)] * self._cols
        return zip_longest(*args, fillvalue=self._fillvalue)
```

..with this `Grid` implementation we can make as many grids we want, just passing to `Grid` the contents and the number of cols:

```python
contents = [
    'One blog post:',
    A(href='www.something.com')('A link to something'),
    Img(src='img'),
    'Some random text',
    None,  # That's an empty cell in the grid
    'Other random text'
]
my_grid = Grid(contents, 3)
my_grid.render(pretty=True)
>>> <div class="container">
>>>     <div class="row">
>>>         <div class="col">One blog post:
>>>         </div>
>>>         <div class="col">
>>>             <a href="www.something.com">A link to something
>>>             </a>
>>>         </div>
>>>         <div class="col"><img src="img"/>
>>>         </div>
>>>     </div>
>>>     <div class="row">
>>>         <div class="col">Some random text
>>>         </div>
>>>         <div class="col">
>>>         </div>
>>>         <div class="col">Other random text
>>>         </div>
>>>     </div>
>>> </div>
```
