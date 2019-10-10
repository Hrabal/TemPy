---
layout: default
---

TemPy documentation
======


```python
from tempy.tags import Html, Head, Body, Meta, Link, Div, P, A
my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']
another_list = ['Lorem ipsum ', 'dolor sit amet, ', 'consectetur adipiscing elit']

page = Html()(  # add tags inside the one you created calling the parent
    Head()(  # add multiple tags in one call
        Meta(charset='utf-8'),  # add tag attributes using kwargs in tag initialization
        Link(href="my.css", typ="text/css", rel="stylesheet")
    ),
    body=Body()(  # give them a name so you can navigate the DOM with those names
        Div(klass='linkBox')(
            A(href='www.foo.com')
        ),
        (P()(text) for text in my_text_list),  # tag insertion accepts generators
        another_list  # add text from a list, str.join is used in rendering
    )
)
```

Build HTML without writing a single tag.

HTML is like SQL: we all use it, we know it works, we all recognize it's important, but our biggest dream is to never write a single line of it again. For SQL we have ORM's, but we're not there yet for HTML.

Templating systems are cool (Python syntax in HTML code) but not cool enough (you still have to write HTML somehow)... That's where the idea of TemPy comes in.

TemPy lets the developer build the DOM using only Python objects and classes. It provides a simple but complete API to dynamically create, navigate, modify and manage HTML templates and objects in pure Python.

TemPy is designed to offer Object Oriented Templating, giving the developer the ability to use and manage HTML templates following the OOP paradigms. Subclassing, overriding and all the other OOP techniques will make HTML templating more flexible and maintainable.

Navigating the DOM and manipulating tags is possible in a Python or jQuery-style syntax. TemPy makes it easier to use different HTML structures for different contents, add dynamic contents and manage every content exception, add dynamic formatting in the template code.

Later, your controllers can serve the page by just calling the `render()` method on the root element, so this code:

```python
Html()(
    Head()(
        Meta(charset="utf-8"),
        Link(href="my.css", typ="text/css", rel="stylesheet")
    ),
    Body()(
        Div(klass="linkBox")(
            A(href="www.foo.com")("A link to www.foo.com"),
            A(href="www.bar.com")("A link to www.bar.com"),
            A(href="www.baz.com")("A link to www.baz.com"),
            A(href="www.python.org")("This is a link to Python")
        ),
        P("This is foo"),
        P("This is Bar"),
        P("Have you met my friend Baz?"),
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    )
).render()
```

Will generate this HTML output:

```html
<html>
    <head>
        <meta charset="utf-8"/>
        <link href="my.css" type="text/css" rel="stylesheet"/>
    </head>
    <body>
        <div class="linkBox">
            <a href="www.foo.com">A link to www.foo.com</a>
            <a href="www.bar.com">A link to www.bar.com</a>
            <a href="www.baz.com">A link to www.baz.com</a>
            <a href="www.python.org">This is a link to Python</a>
        </div>
        <p>This is foo</p>
        <p>This is Bar</p>
        <p>Have you met my friend Baz?</p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit
    </body>
</html>
```



## Speed

TemPy's philosophy is to provide a different approach to HTML generation, with performance in mind.

One of the main factors that leads to slow speeds when developing webapps is the template engine. TemPy has a different approach to HTML generation, resulting in a significant speed boost in many occasions.

No parsing and a simple structure make TemPy fast. TemPy simply adds HTML tags around your data, and the actual HTML string exists only at render time.
