---
layout: default
title: TemPy in Action - TempyREPR
permalink: /make_an_app/tempy_4/
---


# Let's Build an App

### TemPy in Action, TempyREPR

Another way to use TemPy is to define how objects will be rendered in the DOM by defining `TempyREPR` classes inside the object classes. To show how to user `TempyREPR` we'll build the single person's pages using this tecnique.

First, add the controller for the single person page, we already added links to this page in the homepage of our app with link in the form `person/<person_id>`, so we write a controller for those links:

```python
# controllers.py

from app import app, db
from models import Person
from templates.pages import HomePage, PersonPage


@app.route('/')
def index():
    five_people = db.session.query(Person).order_by(Person.second_name, Person.name).limit(5).all()
    return HomePage(data={'people': five_people}).render()


@app.route('/person/<person_id>')
def person(person_id):
    person = db.session.query(Person).filter_by(person_id=person_id).first()
    return PersonPage(data={'person': person}).render()
```

We are using the `PersonPage` template to show the page, so we need to add this import from `templates/pages.py` in which we'll build the new template.

In the `templates/pages.py`file we add the new template with the minimun code to place our person data, leaving the actual person data formatting to a `TempyREPR` placed inside the `Person` model:

```python
class PersonPage(BasePage):
        def init(self):
            self.body.main.container.attr(klass="container")
            self.body.main.container(
                Div(klass='row')(
                    Div(klass='col')(
                        self._data['person']
                    )
                )
            )
```

As you can see we place the `Person` instance directly inside the TemPy class `Div`. TemPy will take care of searching for a `TempyREPR` inside this instance, and use it to add the correct tags inside the page.

So, in our `models.py` we add a representation class for our `Person` model:

```python
# models.py

from tempy import TempyREPR
from tempy.tags import Span, B
from app import db


class Person(db.Model):
    person_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    name = db.Column(db.String(255),
                     index=True,
                     nullable=False)
    second_name = db.Column(db.String(255),
                            index=True)
    birth_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Person: {self.name} {self.second_name}>'

    class PersonREPR(TempyREPR):
        def repr(self):
            self(
                Span(klass='personData')(B()('Name: '), self.name),
                Span(klass='personData')(B()('Second Name: '), self.second_name),
                Span(klass='personData')(B()('Birthday: '), self.birth_date.isoformat())
            )


class Contact(db.Model):
    contact_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    person_id = db.Column(db.Integer,
                          db.ForeignKey('person.person_id'))
    person = db.relationship('Person',
                             backref='contacts',
                             foreign_keys=[person_id])
    contact_type = db.Column(db.String(10),
                             index=True,
                             nullable=False)
    value = db.Column(db.String(255))

    def __repr__(self):
        return f'<Contact {self.contact_type} of {self.person}: {self.value}>'
```

With the nested class `PersonREPR` that inherits from `TempyREPR` we define a way every instance of `Person` will be treated when found inside a TemPy tag.

In this class we just wrote we need to define a `repr` method, in which `self` is both the `Person` instance container (`Div(klass='col')`) and the instance of `Person` itself. We can call `self` to add content where we are placing the `Person` instance and we can access `self` attributes as we would do with a normal `Person` instance.

That's it, now if we restart our webserver, navigate to the home and click on some person's card we'll se that TemPy have rendered the `Person` as serie of `<span>` with strings and the `Person` data inside.

--- 

Now we do the same with `Contact` to add contacts inside a Bootstrap table in the person profile, using another feature of `TempyREPR`: place-awareness.

We add a new `TempyREPR` inside the `Contact` model, calling it `Tr`. We use this name so TamPy knows to choose this repr if a `Contact` is found inside a `tewmpy.tags.Tr` instance.

This is our `Contact` model now:

```python
class Contact(db.Model):
    contact_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    person_id = db.Column(db.Integer,
                          db.ForeignKey('person.person_id'))
    person = db.relationship('Person',
                             backref='contacts',
                             foreign_keys=[person_id])
    contact_type = db.Column(db.String(10),
                             index=True,
                             nullable=False)
    value = db.Column(db.String(255))

    def __repr__(self):
        return f'<Contact {self.contact_type} of {self.person}: {self.value}>'

    class Tr(TempyREPR):
        def repr(self):
            self(
                Td()(self.contact_type.title()),
                Td()(self.value)
            )

```

The `Tr` repr will place two table cells inside the row, with the contact type and the contact value inside. To make this work we just have to add the table in the `PersonPage` template:

```python
class PersonPage(BasePage):
        def init(self):
            self.body.main.container.attr(klass="container")
            self.body.main.container(
                Div(klass='row')(
                    Div(klass='col')(
                        self._data['person']
                    )
                ),
                Div(klass='row')(
                    Div(klass='col')(
                        Table(klass='table')(
                            Tr()(c) for c in self._data['person'].contacts
                        )
                    )
                )
            )

```
