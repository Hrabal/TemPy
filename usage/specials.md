---
layout: default
title: Content and special TemPy Objects
permalink: /usage/specials/
---
## Content

To make a Block a dynamic, so it can contain different contents each request/use, we can use TemPy's `Content` class.

Those elements are just containers with no html representation, at render time this children will be rendered inside the `Content`'s father. `Content` can have a fixed content so it can be used as 'html invisible box' (this fixed content can, however, be dynamic), or it can just have a name.

Every TemPy objects can contain extra data that will not be rendered, you can manage this extra data with the `TemPyClass.data()` api as if it's a common dictionary. At render time TemPy will search into the extra data of the `Content` container, and recursively into his parents, looking for a key matching the `Content`'s name. If it's found then it's value is used in rendering.

<code id='lefty-code'>container = Div()(
    Content(content='This is a fixed content')
)
container.render()
&gt;&gt;&gt; &lt;div&gt;This is a fixed content&lt;/div&gt;
</code>

<code id='lefty-code'>container = Div()(
    Content('a_content_name')
)
container.data({'a_content_name': 'This is dynamic content'})
container.render()
&gt;&gt;&gt; &lt;div&gt;This is dynamic content&lt;/div&gt;
</code>

<code id='lefty-code'>root_container = Span()
container = Div()(
    Content('a_content_name')
)
root_container.append(container)
root_container.inject({'a_content_name': 'This is dynamic content'})
root_container.render()
&gt;&gt;&gt; &lt;span&gt;&lt;div&gt;This is dynamic content&lt;/div&gt;&lt;/span&gt;
</code>


## Escape, sometimes you need it

Another special TemPy class is the `Escaped` class. With this class you can add content that will not be html escaped, it's useful to inject plain html blocks (in string format) into a TemPy tree.

```python
from tempy import Escaped

_ = Div()(Escaped("""<p>
here is some html I had in my closet
</p>
"""))
```