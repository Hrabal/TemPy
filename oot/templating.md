---
layout: default
title: OOT - Object Oriented Templating 
permalink: /oot/templating/
---

We can define a basic `tempy.tags.Html` subclass where we define the basic shared page structure (i.e: header, footer, menu and container div structure) and then use this custom page implementation as a base class for several different pages of our site.

```python
from tempy.widgets import TempyPage

class BasePage(TempyPage):
    def js(self):
        return [
            Script(src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"),
        ]

    def css(self):
        return [
            Link(href=url_for('static', filename='style.css'),
                 rel="stylesheet",
                 typ="text/css"),
            Link(href='https://fonts.googleapis.com/css?family=Quicksand:300',
                 rel="stylesheet"),
            Link(href=url_for('static',
                              filename='/resources/font-awesome-4.7.0/css/font-awesome.min.css'),
                 rel="stylesheet"),
        ]

    # Define the init method as a constructor of your block structure
    def init(self):
        self.head(self.css(), self.js())
        self.body(
            container=Div(id='container')(
                title=Div(id='title')(
                    Div(id='page_title')(A(href='/')('MySite')),
                    menu=self.make_menu('MAIN')
                ),
                content=Div(id='content')(Hr())
            )
        )

    # Your subclass can have his own methods like any other class
    def make_menu(self, typ):
        return Div(klass='menu')(
                            Nav()(
                                Ul()(
                                    Li()(
                                        A(href=item[1])(item[0]))
                                    for item in self.get_menu(typ)
                                )
                            ),
                        )

    def get_menu(self, typ):
        return [(mi.name, mi.link)
                for mi in Menu.query.filter_by(active=True, menu=typ
                                               ).order_by(Menu.order).all()]

class HomePage(BasePage):

    def init(self):
        self.body.container.content(
            Div()(
                Br(),
                'This is my home page content', Br(),
                H3()('Hame page important content'),
                'Look, I\'m a string!', Br(),
                H3()('H3 is big, really big'),
                H1()('Today\'s content:'),
                self.get_dynamic_content()
            )
        )

    def get_dynamic_content(self):
        # Here using SQLAlchemy:
        current_content = Content.query.outerjoin(Content.comments).order_by(Content.date.desc(), Content.id.desc()).limit(1).first()
        if not current_content:
            return 'No content today!'
        return Div()(Span()(current_content.title),
                     Span()(current_content.text)),
                     Div()(comment for comment in current_content.comments))
```

All the work is made defining a custom `init` method. This method will be called when creating new instances of our class, the concept is similar to Python's `__init__` magic method. TemPy executes each base class `init` method in reverse mro, so your subclass can access all the elements defined in his parent classes. It' like the first thing every `init` does is calling `super().init`.