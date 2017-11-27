---
layout: default
title: TemPy API
permalink: /usage/building/api/
---
TemPy lets you build blocks and put them together using the manipulation api.

## Building API

api | action
-------------- | --------------
div1.after(div2) | div1 will be the sibling next to div2 inside div2's container | div1
div1.before(div2) | div1 will be the sibling before div2 inside div2's container | div1
div1.prepend(div2) | div2 will be the first child of div1 | div1
div1.prepend_to(div2) | div1 will be the first child of div2 | div1
div1.append(div2) | div2 will be the last child of div1 | div1
div1.append_to(div2) | div1 will be the list child of div2 | div1
div1.wrap(div2) | div1 will be the only child of div2
div1.wrap_inner(div2) | div1 will be added between div2 and his previous parent
div1.replace_with(div2) | elements will be swapped
div1.remove(div2) | div2 will be removed from div1
div1.move_childs(div2) | all the children of div1 will be moved to div2
div1.move(div2) | div1 will be detached from his father and moved inside div2
div1.pop() | pop by index from div1 children
div1.empty() | deletes all div1 children.

## Traversing API

Every TemPy Tag is iterable and accessible like a Python list, iteration over a TemPy object is an iteration over his children.

```python
container = Div()(Span() for _ in range(2))
for span in container:
    span('some text')
>>> <div><span>some text</span><span>some text</span></div>
```
```python
container = Div()(Span() for _ in range(2))
container[1]('some text')
>>> <div><span></span><span>some text</span></div>
```

It's also possible to access some child by name, as if they're attributes of the parent.
```python
container_div = Div()
container_div(content_div=Div())

container_div.content_div('Some content')
>>> <div><div>Some content</div></div>
```

A jQuery-ish api is given to access TemPy instance's children:
<code id='lefty-code'>container_div.children()
container_div.first()
container_div.last()
container_div.next()
container_div.next_all()
container_div.prev()
container_div.prev_all()
container_div.parent()
container_div.slice(from_index, to_index)
</code>

# API Reference

Several api's are provided to traverse and modify an existing DOM elements, docs ASAP.

For now open your console and `help(tempy.Tag)`.
