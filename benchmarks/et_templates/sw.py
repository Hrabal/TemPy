from lxml import etree as ET
from lxml.builder import E

A = E.a
I = E.i
B = E.b


def CLASS(v):
    # helper function, 'class' is a reserved word
    return {'class': v}


page = (
    E.html(
        E.head(
            E.title("This is a sample document")
        ),
        E.body(
            E.h1("Hello!", CLASS("title")),
            E.p("This is a paragraph with ", B("bold"), " text in it!"),
            E.p("This is another paragraph, with a ",
                A("link", href="http://www.python.org"), "."),
            E.p("Here are some reserved characters: <spam&egg>."),
            ET.XML("<p>And finally, here is an embedded XHTML fragment.</p>"),
        )
    )
)
