---
layout: default
title: Basic Usage
permalink: /usage/
---
# Basic components: TemPy tags

```python
from tempy.tags import *
```

Tag creation is made by instantiating TemPy tags fond in the `tempy.tags` module:

```python
from tempy import tags

my_div = tags.Div()
```

TemPy offers clean syntax for building pages in pure python. Every TemPy object is a container of other (TemPy or not) objects, when rendered TemPy objects will produce an html tag containing the `str` representation of all his children.

```python
from tempy.tags import Div, Span
# Create some TemPy objects/tags
div = Div()()

# Add content inside the created tag
div(Span())

# ..add every kind of object
div('Hello ')
div(1)

# Render starting from the root element
div.render()
>>> <div><span></span>Hello 1</div>
```

TemPy objects can be arranged together dynamically to build the DOM tree. Every TemPy instance is a node of the DOM, and can be father or child of other TemPy objects.

Every instance of a TemPy tag can be created and then later you can put content inside it, or can be put inside another TemPy tag instance.

```python
from tempy.tags import Div, Span, A
# Create empty TemPy instances:
my_span = Span()
my_div = Div()

# Create non-empty TemPy instances:
container = Div()(
    'Hello ', Div()('World!')
)

# Build the TemPy tree putting instances inside one another 
# calling your objects with other objects as arguments
my_div(my_span)
my_span(A(href='www.bar.com')('this is the link text'))

# Add objects inside TemPy instances using a named argument
# so they can be accessed as attributes later
container(test=my_div)
assert container.test == my_div
```

TemPy trees can also be arranged using the TemPy api on every DOM element:

```python
# ..following the code above, you can add content using the append method of the father
container.append(A(href='www.baz.com')('another useful link'))

# Or you can make and add a tag to a container using the append_to method of the child
link = A(href='www.greatsite.com')('GreatWebSite!').append_to(container)
```

Every HTML tag have his corresponding TemPy class, to create a tag just instantiate the TemPy class: `Div()` will produce an object that can contain other objects (TemPy objects or not) and can be rendered into and HTML string.

Once a TemPy tag or widget is instantiated you can add tags and content by calling the instance as if it's a function: `div(Span())`.
Element creation and insertion can be performed in a single instruction: `Div()(Span())`.

It's possible to add elements inside TemPy objects in several ways:

* single objects: `Div()(Span())`
* lists: `Div()(['something', Span(), 1])`
* generators: `Div()(Span() for _ in range(5))`
* single objects with a name (so they can be accessed by name later): `Div()(some_child=Span())`
* or using the TemPy objects's API: `Div().append((Span())` *see below for a complete API listing*

<aside class="warning">Attention: named insertion is safe only using Python >= 3.6</aside>



### Attributes 


TemPy tags can have attributes that will be rendered inside the tag.
HTML tags have attributes, and so TemPy tags have too. It's possible to define tag attributes in different ways:

* during the element instantiation: `Div(some_attribute='some_value')`
* using the `attr` API: `Div().attr(some_attribute='some_value')`

```python
# Add attributes and content to already placed tags
link = A(id='verySpecialId')('This is a link to Python')
link.attr(href='www.python.org')
link.render()
>>> <a id="verySpecialId" href="www.python.org">This is a link to Python</a>
```


### Rendering

The resulting tree is the DOM, and can be rendered by calling the `.render()` method.

```python
# Render your TemPy tree
container.render()
>>><div>content:
>>>    <div>this is the content</div>
>>>    <div>
>>>        <span>
>>>            <a href="www.bar.com">this is the link text</a>
>>>        </span>
>>>        <link href="www.python.org"/>
>>>    </div>
>>>    <a href="www.baz.com">another useful link</a>
>>></div>
```

Calling `render` on some TemPy object will return the html representation of the tree starting from the current element including all the children.
`tempy_object.render()` will:
* render `tempy_object` own tag and  attributes
* loop over `tempy_object` children to retrieve the tag inner content, and for every child:
  * a valid `TempyREPR` is searched inside the child class definition, and used if found to transform a non-TemPy object in a renderable object.
  * a `render` method will be searched and called if present into the child object.
  * if the object is a subclass of `Escaped`, the `Escaped`'s content is returned
  * if no other condition is met, `str()` will be called on the child
* every content found will be joined using `''.join()`
