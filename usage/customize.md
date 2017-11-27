---
layout: default
title: Customizing TemPy Tags
permalink: /usage/customize/
---
## Subclassing Tempy tags

It's possible to define custom tag subclassing either `tempy.elements.Tag` or `tempy.elements.VoidTag` providing a custom `__tag` attribute, a custom `__template` and/or a custom `render` method.
```python
from tempy.elements import Tag

# Making a tag that repeats itself, whi? Because!
class Double(Tag):
    __tag = 'custom'
    def render(self, *args, **kwargs):
        return super().render() * 2

Double()('content').render()
>>> <custom>content</custom><custom>content</custom>
```

## TemPy Tags Factory

Another way to make custom tag is to use the `T` object. The T object is a multi-feature object that work as a class factory for custom tags.

```python
from tempy import T
from tempy.elements import Tag

my_tag = T.Custom
my_tag
>>> <class tempy.t.Custom>
issubclass(my_tag, Tag)
>>> True
my_tag().render()
>>> <custom></custom>

my_tag = T['custom with spaces']
my_tag().render()
>>> <custom with spaces></custom with spaces>

# Same for void tags using the Void specialized class factory
my_void_tag = T.Void.CustomVoid
my_void_tag().render()
>>> <customvoid/>
```

Accessing an attribute/key of the T object will produce a TemPy Tag (of VoidTag) subclass named after the given attribute/key (in lowercase).

Classes made with `T` are subclasses of `tempy.tempy.DOMElement` and behave like any other TemPy Tag, they inherits the api and the features of TemPy objects.


`T` can also produce TemPy tags from html strings on the fly. Using the `from_string` method it converts html strings into a list of TemPy trees:

<code id='lefty-code'>from tempy import T
html_string = '&lt;div&gt;I come from a &lt;i&gt;weird&lt;/i&gt; webservice or from an old file, &lt;b&gt;beware!&lt;/b&gt;&lt;/div&gt;'
parsed = T.from_string(html_string)
div = parsed[0]
div
&gt;&gt;&gt; &lt;tempy.tags.Div 111803135243328262154888799873263607712. 4 childs.&gt;
div[0]
&gt;&gt;&gt; 'I come from a '
div[1]
&gt;&gt;&gt; &lt;tempy.tags.I 42050800055174656216927079271212875762. Son of Div. 1 childs.&gt;
div[1][0]
&gt;&gt;&gt; 'weird'
</code>