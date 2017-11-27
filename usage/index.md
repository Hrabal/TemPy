---
layout: default
title: Basic Usage
permalink: /usage/
---
```python
from tempy.tags import *
```

TemPy offers clean syntax for building pages in pure python. Every TemPy object is a container of other objects, when rendered TemPy objects will produce an html tag containing the `str` representation of all his children.
```python
# Create some TemPy objects/tags
div = Div()(Span())

# Render starting from the root element
div.render()
>>> <div><span></span></div>
```

TemPy objects can be arranged together dynamically to build the DOM tree. Every TemPy instance is a node of the DOM, and can be father or child of other TemPy objects.

```python
# Create non empty TemPy objects/tags
container = Div()(
    'content: ', Div()('this is the content')
)

# Build the TemPy tree calling your objects
div(span)
span(A(href='www.bar.com')('this is the link text'))
container(test=div)
```
TemPy trees can also be arranged using the TemPy api on every DOM element:
```python
container.append(A(href='www.baz.com')('another useful link'))

# If you gave a name to a TemPy object call him by name
link = Link().append_to(container.test)
```

Every HTML tag have his corresponding TemPy class, to create a tag just instantiate the TemPy class: `Div()` will produce an object that can contain other objects (TemPy objects or not) and can be rendered into and HTML string.

TemPy tags can have attributes, that will be rendered inside the tag, it's possible to define attributes when instantiating the object (`Div(attribute='value')`) or later using the api (`Div().attr(attribute='value')`).

Once a TemPy tag or widget is instantiated you can add tags and content by calling the instance as if it's a function: `div(Span())`. Element creation and insertion can be performed in a single instruction: `Div()(Span())`.

It's possible to add elements inside TemPy objects:

* single objects: `Div()(Span())`
* lists: `Div()(['something', Span(), 1])`
* generators: `Div()(Span() for _ in range(5))`
* single objects with a name (so they can be accessed by name later): `Div()(some_child=Span())`
* or using the TemPy objects's API: `Div().append((Span())` *see below for a complete API listing*

<aside class="warning">Attention: named insertion is safe only using Python >= 3.6</aside>



### Attributes 

HTML tags have attributes, and so TemPy tags have too. It's possible to define tag attributes in different ways:

* during the element instantiation: `Div(some_attribute='some_value')`
* using the `attr` API: `Div().attr(some_attribute='some_value')`

```
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
* render `tempy_object` own tag, with foud tag attributes
* loop over `tempy_object` children to retrieve the tag inner content, for every child:
  * a valid `TempyREPR` is searched inside the child class definition, if found it's used.
  * a `render` method will be searched and called if present into the child object.
  * if the object is a subclass of `Escaped`, the `Escaped`'s content is returned
  * if no other condition is met, `str()` will be called on the child
* every content found will be joined using ''.join()