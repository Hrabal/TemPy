---
layout: default
title: TemPy in Action - Dynamic contents
permalink: /make_an_app/tempy_3/
---


# Let's Build an App

### TemPy in Action, dynamic contents: cycles and conditions

Now it's time to add some dynamic contents in our page. We'll get those contents from the databse and we'll use python and TemPy to put those in our template.

First we have to retrieve the data, so we use SQLAlchemy query method to get the first 10 people in our database, sorted by name. We'll do this in our controller:

```python
# controllers.py

from app import app, db
from models import Person
from templates.home import HomePage


@app.route('/')
def index():
    people = db.session.query(Person).order_by(Person.second_name, Person.name).limit(9).all()
    return HomePage(data={'people': people}).render()
```

We added two new imports:
 * `db` from the `app.py` module
 * `Person` from our models

We use the `db.session.query` method to start a query to the db, and then we apply a sorting to our records with `order_by` and a maximum number of records with `limit`. `all()` will run our query and so `people` will contain all the extracted records.

The we pass this data (those are `models.Person` instances) to our template, so we can use them as we please, when instantiating the template with the argument `data={'people': people}`.
This will populate the `content_data` attribute inside our template with the dict we pass to it, so we can retrieve the data while building the DOM.

Now in the `HomePage` template we are going to use this data, this will be the final code of our `HomePage` template:

```python
# templates/home.py

from tempy.tags import Div, P, I, A
from .base import BasePage, CONTACTS_ICONS


class HomePage(BasePage):
    def init(self):
        self.body.main.container.attr(klass="album py-5 bg-light")
        self.body.main.container(
            Div(klass="container")(
                Div(klass='row')(
                    persons=[
                        Div(klass='col-md-4')(
                            Div(klass='card mb-4 shadow-sm')(
                                A(href=f'person/{person.person_id}')(
                                    Div(klass='card-body')(
                                        P(klass='card-text')(
                                            f'{person.name.title()} {person.second_name.title()}'
                                        ),
                                        contacts=[
                                            Div(klass='contactIcon')(
                                                I(klass=CONTACTS_ICONS.get(contact.contact_type, 'noIcon'))
                                            ) for contact in person.contacts
                                        ]
                                    )
                                )
                            )
                        ) for person in self.content_data['people']
                    ]
                )
            )
        )
```

The basic Bootstrap structure consists of three nested divs with the classes `container`, `row` and `col` inside a div with the `album py-5 bg-light` css class. From the previous part of this tutorial we already have a div in which we can place our content in the `self.body.main.container` attribute path so we change the css class of this empty div we created in the `BasePage` template with the class we need in the home page of our app:

```python
self.body.main.container.attr(klass="album py-5 bg-light")
```

We access the already created div by names, and we call the TemPy method `attr` on this TemPy tag, that will translate this call arguments to attributes of the TemPy tag.

Then we add content inside this div by calling this function:

```python
self.body.main.container(
    Div(klass="container")(
        Div(klass='row')(
```
This code will place a div with the Bootstrap's css class "container" the `body.main.container` div, and another div with the css class "row" inside it.

We build the basic Boostrap Grid System scheleton, we now have to add a variable number of cols inside id. To do so we add inside the `row` a named argument called `persons` which is a list comprehension:

```python
[<some tags> for person in self.content_data['people']]
```

`<some tags>` are the basic card structure (from the Bootstrap example) of the list we are building with a link we add so we can click on the card to go tho a single person profile and a couple FontAwesome icons to indicate which kind of contacts we have for this person.

This structure would look like this in plain html:

```html
<div class='col-md-4'>
    <div class='card mb-4 shadow-sm'>
        <a href='person/{id of that person}'>
            <div class='card-body'>
                <p>{name of the person} {second name of the person}</p>
                <div class='contactIcon'><i class='{icon class of the type of this contact}'></div>
                <div class='contactIcon'><i class='{icon class of the type of this contact}'></div>
            </div>
        </a>
    </div>
</div>
```

This repeated for each person, with each contact structure repeated for each person's contact. With TemPy we can translate this into a list comprehension:

```python
[
    Div(klass='col-md-4')(
        Div(klass='card mb-4 shadow-sm')(
            A(href=f'person/{person.person_id}')(
                Div(klass='card-body')(
                    P(klass='card-text')(
                        f'{person.name.title()} {person.second_name.title()}'
                    ),
                    contacts=[
                        Div(klass='contactIcon')(
                            I(klass=CONTACTS_ICONS.get(contact.contact_type, 'noIcon'))
                        ) for contact in person.contacts
                    ]
                )
            )
        )
    ) for person in self.content_data['people']
]
```

As you can see we are looping over the list inside `self.content_data['people']` which is the results of the query we performed in the controller. For each person in our list we are addin the basic structure with a custom link `href` taken from the `person.person_id` attribute we defined in the `Person` model.

Inside this basic structure for each person we are adding another nested list comprehension for the person's contact:

```python
[
    Div(klass='contactIcon')(
        I(klass=CONTACTS_ICONS.get(contact.contact_type, 'noIcon'))
    ) for contact in person.contacts
]
```

`CONTACT_ICONS` is a mapping we define in our `templates/base.py` file, that now looks like this:

```python
# templates/base.py

from app import app
from flask import url_for
from tempy.widgets import TempyPage
from tempy.tags import Link, Script, Meta, Main, Section, Div, H1, P

CONTACTS_ICONS = {
    'email': 'fas fa-envelope',
    'phone': 'fas fa-phone',
    'mobile': 'fas fa-mobile',
    'facebook': 'fab fa-facebook-square'
}

with app.test_request_context():
    HEAD_TAGS = [
        Meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no"),
        Link(rel="stylesheet",
             href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
             integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb",
             crossorigin="anonymous"),
        Link(rel="stylesheet", href=url_for('static', filename='style.css'), typ="text/css")
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
           crossorigin="anonymous"),
    Script(defer=True, src="https://use.fontawesome.com/releases/v5.0.0/js/all.js")
]


class BasePage(TempyPage):
    def init(self):
        self.head(HEAD_TAGS)
        self.body(
            main=Main(role='main')(
                header=Section(klass="jumbotron text-center")(
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

Notice that we added the mapping, but also we added a `Link` inside the `HEAD_TAGS`. This new link is the import of our custom css file, that we retrieve using Falsk's `url_for` method. We call `url_for` inside the `with app.test_request_context()` for Flask needs it to generate a valid url for our static files.

So, add this in a new file called `style.css` inside the `static` folder:

```css
.contactIcon {
    padding-left: 1em;
    float: right;
}
```

Now if we start again our app with `python run.py` in the terminal and hit the `http://localhost:5000/` we can see that the page now have a colum for each person, with variable icons depending on the person's contacts.

In the [next section](../tempy_4/) we'll use another TemPy feature, `TempyREPR`, that will let us define a TemPy structure directly in the models.
