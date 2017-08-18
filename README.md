# TemPy
[![Build Status](https://travis-ci.org/Hrabal/TemPy.svg?branch=master)](https://travis-ci.org/Hrabal/TemPy) 
![TemPy Logo](tempy.png)

### Fast Object-Oriented HTML templating With Python!

### What
Build HTML without writing a single tag.
TemPy dynamically generates HTML and accesses it in a pure Python or jQuery fashion. Navigating the DOM and manipulating tags is also possible in a Python or jQuery-similar sintax.

### Why?
HTML is like SQL: we all use it, we know it works, we all recognize it's important, but our biggest dream is to never write a single line of it again. For SQL we have ORM's, but we're not there yet for HTML.
Templating systems are cool (Python syntax in html code) but not cool enough (you still have to write html somehow)..
..so the idea of TemPy.

### Weeeeeeee!
No parsing and a simple structure makes TemPy fast. TemPy simply adds html tags around your data, and the actual html string exists only at render time.
See below for benchmarks against other templating engines.

**Build, manipulate, and navigate HTML documents. With no HTML involved.**

# Usage
### Installation
TemPy is avaiable on PyPi: `pip3 install tem-py`.

Or clone/download this repository and run `python3 setup.py install`

### Basic Templating

TemPy offers clean syntax for building pages in pure python:
```python
from tempy.tags import Html, Head, Body, Meta, Link, Div, P, A
my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']
another_list = ['Lorem ipsum ', 'dolor sit amet, ', 'consectetur adipiscing elit']

# make tags instantiating TemPy objects
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

# add tags and content later
page[1][0](A(href='www.bar.com'))  # calling the tag
page[1][0].append(A(href='www.baz.com'))  # using the API
link = Link().append_to(page.body) # access the body as if it's a page attribute
link.attr(href='www.python.org')('This is a link to Python') # Add attributes and content to already placed tags

page.render()
>>> <html>
>>>     <head>
>>>         <meta charset="utf-8"/>
>>>         <link href="my.css" type="text/css" rel="stylesheet"/>
>>>     </head>
>>>     <body>
>>>         <div class="linkBox">
>>>             <a href="www.foo.com"></a>
>>>             <a href="www.bar.com"></a>
>>>             <a href="www.baz.com"></a>
>>>             <a href="www.python.org">This is a link to Python</a>
>>>         </div>
>>>         <p>This is foo</p>
>>>         <p>This is Bar</p>
>>>         <p>Have you met my friend Baz?</p>
>>>         Lorem ipsum dolor sit amet, consectetur adipiscing elit
>>>     </body>
>>> </html>
```

#### Building blocks
You can also create blocks and put them together using the manipulation api:
```python
# --- file: base_elements.py
from somewhere import links, foot_imgs
# define some common blocks
header = Div(klass='header')(title=Div()('My website'), logo=Img(src='img.png'))
menu = Div(klass='menu')(Li()(A(href=link)) for link in links)
footer = Div(klass='coolFooterClass')(Img(src=img) for img in foot_imgs)
```
```python
# --- file: pages.py
from base_elements import header, menu, footer

# import the common blocks and use them inside your page
home_page = Html()(Head(), body=Body()(header, menu, content='Hello world.', footer=footer))
content_page = Html()(Head(), body=Body()(header, menu, container=Div(klass='container'), footer=footer))
```
```python
# --- file: my_controller.py
from tempy.tags import Div
from pages import home_page, content_page

@controller_framework_decorator
def mycontroller(url='/'):
    return home_page.render()

@controller_framework_decorator
def mycontroller(url='/content'):
    content = Div()('This is my content!')
    return content_page.body.container.append(content).render()
```

### Elements creation and removal
Create DOM elements by instantiating tags:
```python
page = Html()
>>> <html></html>
```

Add elements or content by calling them like a function...
```python
page(Head())
>>> <html><head></head></html>
```
...or use one of the jQuery-like apis:
```python
body = Body()
page.append(body)
>>> <html><head></head><body></body></html>

div = Div().append_to(body)
>>> <html><head></head><body><div></div></body></html>
div.append('This is some content', Br(), 'And some Other')
>>> <html><head></head><body><div>This is some content<br>And some Other</div></body></html>
```
...same for removing:
```python
head.remove()
>>> <html><body><div></div></body></html>
body.empty()
>>> <html><body></body></html>
page.pop()
>>> <html></html>
```

All the main jQuery manipulating apis are provided.


## Tag Attributes 
Add attributes to every element at definition time or later:
```python
div = Div(id='my_html_id', klass='someHtmlClass') # 'klass' because 'class' is a Python's buildin keyword
>>> <div id="my_dom_id" class="someHtmlClass"></div>

a = A(klass='someHtmlClass')('text of this link')
a.attr(id='another_dom_id')
a.attr({'href': 'www.thisisalink.com'})
>>> <a id="another_dom_id" class="someHtmlClass" href="www.thisisalink.com">text of this link</a>
```

Styles are editable in the jQuery fashion:
```python
div2.css(width='100px', float='left')
div2.css({'height': '100em'})
div2.css('background-color', 'blue')
>>> <div id="another_dom_id" class="someHtmlClass comeOtherClass" style="width: 100px; float: left; height: 100em; background-color: blue"></div>
```

### DOM navigation

Every TemPy Tag content is iterable and accessible like a Python list:
```python
divs = [Div(id=div, klass='inner') for div in range(10)]
ps = (P() for _ in range(10))
container_div = Div()(divs)

for i, div in enumerate(container_div):
    div.attr(id='divId'+str(i))
container_div[0].append(ps)
container_div[0][4].attr(id='pId')
>>> <div>
>>>     <div id="divId0">
>>>         <p></p>
>>>         <p></p>
>>>         <p></p>
>>>         <p></p>
>>>         <p id="pId"></p>
>>>         <p></p>
>>>         <p></p>
>>>         <p></p>
>>>         <p></p>
>>>         <p></p>
>>>     </div>
>>>     <div id="divId1"></div>
>>>     <div id="divId2"></div>
>>>     <div id="divId3"></div>
>>>     <div id="divId4"></div>
>>>     <div id="divId5"></div>
>>>     <div id="divId6"></div>
>>>     <div id="divId7"></div>
>>>     <div id="divId8"></div>
>>>     <div id="divId9"></div>
>>> </div>
```

...or access elements inside a container as if it they were attributes:
```python
container_div = Div()
container_div(content_div=Div())

container_div.content_div('Some content')
>>> <div><div>Some content</div></div>
```


..or if you feel jQuery-ish you can use:
```python
container_div.children()
container_div.first()
container_div.last()
container_div.next()
container_div.prev()
container_div.prev_all()
container_div.parent()
container_div.slice()
```

# Performance
Performance varies considerably based on the complexity of the rendered content, the amount of dynamic content on the page, the size of the produced output and many other factors.

TemPy does not parse strings, does not use regex and does not load .html files, resulting in great speed compared to the traditional frameworks such as Jinja2 and Mako.

Here are a few benchmarks of TemPy in action, rendering a template with a single for loop (see code [here](benchmarks))
Used HW: 2010 IMac, CPU:2,8 GHz Intel Core i7 RAM:16 GB 1067 MHz DDR3 Osx: 10.12.6.
Benchmark made using [WRK](https://github.com/wg/wrk)

Running 20s test @ http://127.0.0.1:8888/tempy + http://127.0.0.1:8888/j2
  10 threads and 200 connections


Tempy | Avg | Stdev | Max | +/- Stdev
----- | --- | ----- | --- | ---------
Latency | 109.55ms | 52.04ms | 515.33ms | 93.09%
Req/Sec | 118.27 | 37.36 | 240.00 | 73.77%

16111 requests in 20.09s, 96.23MB read
Requests/sec: 801.91
Transfer/sec: 4.79MB

Jinja2 | Avg | Stdev | Max | +/- Stdev
----- | --- | ----- | --- | ---------
Latency | 216.04ms | 16.05ms | 267.06ms | 91.16%
Req/Sec | 59.29 | 20.53 | 151.00 | 71.23%

11841 requests in 20.08s, 72.80MB read
Requests/sec:    589.70
Transfer/sec:      3.63MB

## Credits: made and mantained by Federico Cerchiari / Hrabal
### Contribute.
Any contribution is welcome. Please refer to the [contributing page](CONTRIBUTING.md).

## Python versions compatibility
Python >= 3.3 needed, ask [Travis](https://travis-ci.org/Hrabal/TemPy) [![Build Status](https://travis-ci.org/Hrabal/TemPy.svg?branch=master)](https://travis-ci.org/Hrabal/TemPy)

### Apache 2.0 license, see LICENSE for details.
