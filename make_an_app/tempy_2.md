---
layout: default
title: TemPy in Action - Inheritance
permalink: /make_an_app/tempy_2/
---

# Let's Build an App

### TemPy in Action, inheritance and reusability

If we have to build another page, say the "contact" page to diplay the details of a contact, we'd have to re-write pretty much all the code we wrote for our home page. Some of the tags we wrote will never change, and will be the same in every page, for instance the `<link>` and `<script>` tags.

To avoid all this boilerplate code, and to optimize our app's performance, we're going to move our fixed tags outside of the templates so they will be created once and used multiple times, and we are going to make a base template class that will be used in every page.

First, we're going to move all scripts and the link outside the template class, make a new file in the `templates` folder so we can store the common parts of our templates in it:

```python
# base.py

from tempy.tags import Meta, Link, Script

HEAD_TAGS = [
    Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
    Link(rel="stylesheet",
         href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
         integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb",
         crossorigin="anonymous")
]

SCRIPTS = [
    Script(src="https://code.jquery.com/jquery-3.2.1.min.js",
           integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=",
           crossorigin="anonymous"),
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js",
           integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh",
           crossorigin="anonymous"),
    Script(src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
           integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ",
           crossorigin="anonymous")
]
```

In this file we build the `Script`, `Meta` and `Link` tags once, so they are instantiated when our webserver starts and not during each web request. We can then use our `head_tags` and `scripts_tags` in any template just by inserting them in a TemPy tag.

Here's how we do it, again in the `templates/base.py` file we move the basic structure of our site in a base template that we are going to use as a base class for all our templates:

```python
# base.py

from tempy.widgets import TempyPage
from tempy.tags import Link, Script, Meta, Main, Section, Div, H1, P

HEAD_TAGS = [
    Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
    Link(rel="stylesheet",
         href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
         integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb",
         crossorigin="anonymous")
]

SCRIPTS = [
    Script(src="https://code.jquery.com/jquery-3.2.1.min.js",
           integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=",
           crossorigin="anonymous"),
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js",
           integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh",
           crossorigin="anonymous"),
    Script(src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
           integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ",
           crossorigin="anonymous")
]


class BasePage(TempyPage):
    def init(self):
        self.head(HEAD_TAGS)
        self.body(
            main=Main(role='main')(
                Section(klass="jumbotron text-center")(
                    Div(Klass="container")(
                        H1(klass="jumbotron-heading")('TemPy Contact Book'),
                        P(klass="lead text-muted")("A contact book made with TemPy."),
                    )
                ),
                container=Div()
            ),
            scripts=SCRIPTS
        )
```

We defined a `BasePage` class with almost identical struture to `HomePage` defined before. The only differencies are that instead of defining the `Script`, `Meta` and `Link` tags inside our temlate, we define them early and we inseet them in our template. this way when `base.py` is imported (most surely when our app starts) those tags are created and the the same objects are shared between each request.

The other difference is that we gave a couple of names to some tags and we replaced the main page's main content with an empty div:

```python
...
        self.body(
            main=Main(role='main')(
...
                container=Div()
...
```

Adding those child tags using named arguments will let us reach them much more easily later. In fact, now that we created a base template we can change our `HomePage` in `home.py` so it uses this base template and just add the page-specific content:

Our `home.py` will look like this now:

```python
# home.py

from tempy.tags import Div

from .base import BasePage


class HomePage(BasePage):
    def init(self):
        self.head(
        )
        self.body.main.container(
            Div(klass="album py-5 bg-light")(
                Div(klass="container")
            )
        )
```

In the [next section](../tempy_3/) we'll make add to our templates the code needed to display our dynamic contents.
