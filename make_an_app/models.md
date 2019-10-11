---
layout: default
title: The models
permalink: /make_an_app/models/
---

# Let's Build an App

### Models for our App

Our database is currently empty because we haven't added any tables. To do so we'll add some models to our app. SQLAlchemy will take care of all the needed db instructions to create the tables for our models.

These models describe the entities we are going to use in our app. For a basic Contact Book, the models are:

 * Person
 * Contact

Let's open the `models.py` file and add these models:

```python
# models.py

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

With these models we are able to represent a person and n contacts linked to that person. To see if the models are working we have to upgrade our db so the two tables are created:

```shell
(venv)$ python db_update.py
(venv)$ python db_migrate.py
```

Now, to test the model, we'll add a couple of records. Open a python interpreter and add a few people with their contacts (I'm using my favourite Czech writers but feel free to use other people):
```python
(venv)$ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> from models import Person, Contact
>>> from datetime import date
>>> # Make some instances of Person and Contact
>>> bohumil = Person(name='Bohumil', second_name='Hrabal', birth_date=date(1914, 3, 28))
>>> franz = Person(name='Franz', second_name='Kafka', birth_date=date(1883, 7, 3))
>>> pavel = Person(name='Pavel', second_name='Řezníček', birth_date=date(1942, 1, 30))
>>> egon = Person(name='Egon', second_name='Bondi', birth_date=date(1930, 1, 20))
>>> bohu_mail = Contact(person=bohumil, contact_type='email', value='bohumil@hrabal.com')
>>> franz_mail = Contact(person=franz, contact_type='email', value='frankie@czeckpeople.cz')
>>> franz_phone = Contact(person=franz, contact_type='phone', value='0048 0021 99 777')
>>> franz_mobile = Contact(person=franz, contact_type='mobile', value='320 12 13 144')
>>> bohu_phone = Contact(person=bohumil, contact_type='phone', value='0048 0022 98 788')
>>> pavel_mobile = Contact(person=pavel, contact_type='mobile', value='0048 347 66 666')
egon_facebook = Contact(person=egon, contact_type='facebook', value='https://www.facebook.com/profile.php?id=111222333'>>> )
>>> # Save the new entries to the databse
>>> db.session.add(bohumil)
>>> db.session.add(franz)
>>> db.session.add(egon)
>>> db.session.add(pavel)
>>> db.session.add(bohu_mail)
>>> db.session.add(franz_mail)
>>> db.session.add(bohu_mail)
>>> db.session.add(franz_phone)
>>> db.session.add(franz_mobile)
>>> db.session.add(bohu_phone)
>>> db.session.add(pavel_mobile)
>>> db.session.add(egon_facebook)
>>> db.session.commit()
>>> # Check the result
>>> bohu_mail
<Contact email of <Person: Bohumil Hrabal>: bohumil@hrabal.com>
```


Now we are ready to make some pages of our app that will display the models we just created in the [next section](../tempy/).
