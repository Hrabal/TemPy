---
layout: default
title: TemPy REPR
permalink: /oot/tempyrepr/
---
```python
class MyClass:
    def __init__(self):
        self.foo = 'foo'
        self.bar = 'bar'
        self.link = 'www.foobar.com'

    class Div(TempyREPR):
        def repr(self):
            # When a MyClass is placed inside a <div> tag, we add 2 other divs inside with some of our MyClass instance values
            self(
                Div()(self.foo),
                Div()(self.bar)
            )

    class HtmlREPR(TempyREPR):
        def repr(self):
            # We can use HtmlREPR as a fallback for html representation
            self(
                Div()(self.foo),
                Div()(self.bar)
            )

    class A(TempyREPR):
        def repr(self):
            # note: This TempyREPR will be used when placing an instance of MyClass inside a Tempy A instance
            # self here will be the instance of MyClass but using the TemPy api we can modify the parent <a> tag
            self.parent.attrs['href'] = self.link
            self('Link to ', self.bar)

    class Td(TempyREPR):
        def repr(self):
            # we define a custom representation when a MyClass is placed inside a <td>
            self(self.bar.upper())

    class HomePage(TempyREPR):
        def repr(self):
            # HomePage is supposed to be the name of the TemPy root used to rendere the home page
            # when a MyClass is placed anywhere inside the home page this repr will be used
            # note: here self is the object's parent, not the root
            self('Hello World, this is bar: ', self.bar)


my_instance = MyClass()

Div()(my_instance).render()  # my_instance is rendered using Div(TempyREPR) nested class

A()(my_instance).render()  # my_instance is rendered using A(TempyREPR) nested class

my_list = [MyClass() for _ in range 10]
Table()(Tr()(Td()(instance)) for instance in my_class_list).render()  # Td(TempyREPR) is used.

class HomePage(Html): pass

HomePage()(
    Head()(),
    Body()(
        Div()(
            H1()(my_instance)
        )
    )
).render()  # my_instance is rendered using HomePage(TempyREPR) nested class
```

Another way to use TemPy is to define a nested `TempyREPR` subclass inside your own classes.

You can think the `TempyREPR` nested class as a `__repr__` magic method equivalent: TemPy uses the `TempyREPR` nested class to represent objects just like Python uses the `__repr__` method.

When an object is placed inside a tree TemPy searches for a `TempyREPR` class inside this object, if it's found, the `repr` method of this class is used as a template.
The `TempyREPR.repr` method accepts `self` as the only argument, with a little magic this `self` is both your object and the tree element, so the TemPy API is available and your object attributes are accessible using `self`.

You can define several `TempyREPR` nested classes, TemPy will search for a `TempyREPR` subclass following this priority order:

1. a `TempyREPR` subclass with the same name of his TemPy container
2. a `TempyREPR` subclass with the same name of his TemPy container's root
3. a `TempyREPR` subclass named `HtmlREPR`
4. the first `TempyREPR` found.
5. if none of the previous if found, the object will be rendered calling his `__str__` method

You can use this order to set different renderings for different situation/pages. Here is an example of how `TempyREPR` would work with SQLAlchemy models:

<code id='lefty-code'>from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
</code>
<code id='lefty-code'>
class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
</code>
<code id='lefty-code'>    class HtmlREPR(TempyREPR):
        def repr(self):
            self.attr(klass='department')
            self(self.name.title())
</code>
<code id='lefty-code'>
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                         uselist=True,
                         cascade='delete,all'))
</code>
<code id='lefty-code'>    class Table(TempyREPR):
        def repr(self):
            self(
                Tr()(
                    Td()(self.id),
                    Td()(self.name),
                    Td()(self.hired_on.strftime('%Y-%m-%d'))
                )
            )
</code>
<code id='lefty-code'>    class EmployeePage(TempyREPR):
        def repr(self):
            self(
                Div(klass='employee')(
                    Div()('Name: ', self.name),
                    Div()('Department: ', self.department),
                )
            )
</code>

Adding one or more `TempyREPR` into your models will provide the ability to just put instances of those models inside the DOM directly, and they will be rendered according to they're location.

So making a table of employees will be very easy:
<code id='lefty-code'>from tempy.tags import Table
employees_table = Table()(Employee.query.all())</code>

And making a employee page will be easy as well:
<code id='lefty-code'>from tempy.widgest import TempyPage
page = TempyPage().body(Employee.query.first())
</code>

