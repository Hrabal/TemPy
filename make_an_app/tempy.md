---
layout: default
title: TemPy in Action - Basics
permalink: /make_an_app/tempy_base/
---

# Let's Build an App

### TemPy in Action, the basics

In this section we'll start to use TemPy, we're going to build the home page of our site.
To build our app we'll use Bootstrap 4.1, following the recipe in the [Bottstrap's Album Example](https://getbootstrap.com/docs/4.1/examples/album/). We'll recreate the html structure of this example with TemPy and in the next section we'll add our custom contents.

First, we have to make our `templates` folder a valid python module, so we can later import the templates and pages:

```shell
(venv)$ touch templates/__init__.py
```

Now it's time to build our home page structure! Create a file called `home.py` and add this code in it (we'll analyze each line later):

```python
# templates/home.py

from tempy.tags import Link, Script, Meta, Main, Section, Div, H1, P
from tempy.widgets import TempyPage


class HomePage(TempyPage):
    def init(self):
        self.head(
            Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
            Link(rel="stylesheet",
                 href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
                 integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb",
                 crossorigin="anonymous"),
        )
        self.body(
            Main(role='main')(
                Section(klass="jumbotron text-center")(
                    Div(Klass="container")(
                        H1(klass="jumbotron-heading")('TemPy Contact Book'),
                        P(klass="lead text-muted")("A contact book made with TemPy."),
                    )
                ),
                Div(klass="album py-5 bg-light")(
                    Div(klass="container")
                )
            ),
            Script(src="https://code.jquery.com/jquery-3.2.1.min.js",
                   integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=",
                   crossorigin="anonymous"),
            Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js",
                   integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh",
                   crossorigin="anonymous"),
            Script(src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
                   integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ",
                   crossorigin="anonymous"),
        )

```

So much going on here! First things first, the imports:

```python
from tempy.tags import Link, Script, Meta, Main, Section, Div, H1, P
from tempy.widgets import TempyPage
```

Here we are importing from TemPy two different things that are really just the same thing: some tags and a widget.
`tempy.tags` contains the the basic bricks that will form our page, with TemPy all we are going to do is to nest tags and contents inside other tags.

Each tag in the `tempy.tags` is a subclass of `Tag`, the only diferencee between one another is how they will be rendered: `Div` will produce the string `<div></div>`, `P` will produce `<p></p>` and `Link` will produce `<link>`.

We are also importing a class from `tempy.widgets`, in this module we can find a collection of widgets that can be considered as "tags on steroids". Those are subclasses of various tags, with some extra useful methods or behavior. For instance we are importing `TempyPage` which is a subclass of `tempy.tags.Html` with a couple methods to set some common html attributes and the two main parts of an html page already setted and ready to be used: the `head` with his `title` and the `body`.

To see what's a Widget we can try to render an empty widget from the interpreter:
```python
(venv)$ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from tempy.widgets import TempyPage
>>> print(TempyPage().render(pretty=True))
```

That will produce this:

```html
<!DOCTYPE HTML>
<html>
    <head><meta charset="UTF-8"/><meta name="description"/><meta name="keywords"/>
        <title>
        </title>
    </head>
    <body>
    </body>
</html>
```

As you can see TempyPage is a simple html structure that we can use to build our own page. To do so we create our own TemPy class:

```python
class HomePage(TempyPage):
    def init(self):
        pass
```

We can repeat the test above in the shell using `HomePage` instead of `TempyPage` and we'll have the same result. All the custom contents are added in the `init` method, which will be called by TemPy when a `HomePage` instance is created. Let's try it:

```python
class HomePage(TempyPage):
    def init(self):
        self.head(
            Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no")
        )
```

The code above will add a `<meta>` tag with `name` and `content` attributes inside the `<head>` of our document. We did so calling the `head` attribute of our `TempyPage` which is a `tempy.tags.Head` instance. 

The above class will produce the following output, which is the same as our empty `TempyPage` above, with our new `<meta>` tag at the end ot the `<head>` tag:

```html
<!DOCTYPE HTML>
<html>
    <head><meta charset="UTF-8"/><meta name="description"/><meta name="keywords"/>
        <title>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
    </head>
    <body>
    </body>
</html>
```

Each named argument passed to the `Meta` instance will become a tag's attribute, so we do the same adding the `<link>` to Bootstrap's CDN:

```python
class HomePage(TempyPage):
    def init(self):
        self.head(
            Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
            Link(rel="stylesheet",
                 href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
                 integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb",
                 crossorigin="anonymous"),
        )
```

```html
<!DOCTYPE HTML>
<html>
    <head><meta charset="UTF-8"/><meta name="description"/><meta name="keywords"/>
        <title>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous"/>
    </head>
    <body>
    </body>
</html>
```

Notice that we added a comma after the `Meta` instance, because this instance and the `Link` instance are arguments of the method call on `self.head`.

In the next lines we do the same inside the `<body>` tag, the main content section (for the sake of this tutorial we skipped the header of the Bootstrap example) and the Javascript scripts of Bootstrap and JQuery:

```python
        self.body(
            Main(role='main')(
                Section(klass="jumbotron text-center")(
                    Div(Klass="container")(
                        H1(klass="jumbotron-heading")('TemPy Contact Book'),
                        P(klass="lead text-muted")("A contact book made with TemPy."),
                    )
                ),
                Div(klass="album py-5 bg-light")(
                    Div(klass="container")
                )
            ),
            Script(src="https://code.jquery.com/jquery-3.2.1.min.js",
                   integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=",
                   crossorigin="anonymous"),
            Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js",
                   integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh",
                   crossorigin="anonymous"),
            Script(src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
                   integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ",
                   crossorigin="anonymous")
        )
```

One important thing here: in our `Div`s and in the `Section` we used `klass` instead of `class` to specify the css class in the resulting html. This because `class` is a reserved word in Python, so TemPy will always translate `klass` to `class`.

In these lines we added the `<main>` tag inside the `<body>` tag, and while doing so we added other tags inside the newly created `<main>` tag.

Now that we built a TemPy template, we ca use it in our app, go back to the `controllers.py` file, import our `HomePage` and change our handler so it redenders our template:

```python
from app import app

from templates.home import HomePage


@app.route('/')
def index():
    return HomePage().render()
```

Check if everything is working by starting again our app:

```shell
(venv)$ python run.py
WARNING:werkzeug: * Debugger is active!
```

and reload the page on the browser, you should see a page like this:

<img src="{{site.baseurl}}/assets/img/home_page_1.png">

In the [next section](../tempy_2/) we'll make another page learning how inheritance work in TemPy, and how to reuse static blocks of code.
