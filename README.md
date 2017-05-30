# pyQuery
### Html templating with no html involved!

### What
Build HTML without writing a single tag.
pyQuery lets you dynamically generate HTML and accessing it in a jQuery fashion, navigating the tags and manipulating them in pure python.

### Why?
HTML is like SQL: we all know him, we all recognize his importance, we all wish to never write a single tag anymore.
Templating systems are cool (Python syntax in html code) but not cool enough (still html)..
..so the idea of pyQuery.

# Usage:

## Elements creation and removal
You can create a DOM elements instantiating tags:
```
page = Html()
>>> <html></html>
```

You can then add elements or content calling them (just like a function)...
```
page(Head())
>>> <html><head></head></html>
```
..or you can use one of the jQuery-like apis:
```
body = Body()
page.append(body)
>>> <html><head></head><body></body></html>

div = Div().append_to(body)
>>> <html><head></head><body><div></div></body></html>
div.append('This is some content', Br(), 'And some Other')
>>> <html><head></head><body><div>This is some content<br>And some Other</div></body></html>
```
..same for removing:
```
head.remove()
>>> <html><body><div></div></body></html>
body.empty()
>>> <html><body></body></html>
page.pop()
>>> <html></html>
```

## Attributes attribuition 
You can add attributes to every element at definition time or later:
```
div = Div(id='my_html_id', klass='someHtmlClass')
>>> <div id="my_dom_id" class="someHtmlClass"></div>

div2 = Div(klass='someHtmlClass')
div2.attr(id='another_dom_id')
>>> <div id="another_dom_id" class="someHtmlClass comeOtherClass"></div>
```

## "Navigating the DOM"

Every pyQuery Tag is iterable and accessible just like a list:
```
divs = [Div(id=div, klass='inner') for div in range(10)]
ps = (P() for _ in range(10))
container_div = Div()(divs)

for i, div in enumerate(container_div):
    div.attr(id='divId'+i)
container_div[0].append(ps)
container_div[0][4].attr(id='pId')
>>> <div>
>>> 	<div id="divId0">
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p id="uniquePid"></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 		<p></p>
>>> 	</div>
>>> 	<div id="divId1"></div>
>>> 	<div id="divId2"></div>
>>> 	<div id="divId3"></div>
>>> 	<div id="divId4"></div>
>>> 	<div id="divId5"></div>
>>> 	<div id="divId6"></div>
>>> 	<div id="divId7"></div>
>>> 	<div id="divId8"></div>
>>> 	<div id="divId9"></div>
>>> </div>
```

pyQuery offers a rather clean syntax for building pages in just python:
```
my_text_list = ['This is foo', 'This is Bar', 'Have you met my friend Baz?']
page = Html()(
    Head()(
        Meta(charset='utf-8'),
        Link(href="my.css", typ="text/css", rel="stylesheet")
    ),
    Body()(
        Div(klass='linkBox')(
            A(href='www.foo.bar')
        ),
        (P()(my_text_list[i]) for i in range(2))
    )
).render(pretty=True)
>>> <html>
>>> 	<head>
>>> 		<meta charset="utf-8"/>
>>> 		<link href="my.css" type="text/css" rel="stylesheet"/>
>>> 	</head>
>>> 	<body>
>>> 		<div class="linkBox">
>>> 			<a href="www.foo.bar"></a>
>>> 		</div>
>>> 		<p>This is foo</p>
>>> 		<p>This is Bar</p>
>>> 		<p>Have you met my friend Baz?</p>
>>> 	</body>
>>> </html>
```
