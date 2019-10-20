
# Bootstrap Starter template into TemPy 
# Source: https://getbootstrap.com/docs/4.3/getting-started/introduction/

from tempy.tags import *

page = Html(lang='en')
head = Head()(
            Comment(" Required meta tags "),
            Meta(charset='utf-8'),
            Meta(name="viewport"),
            Comment(" Bootstrap CSS "),
            Link(rel="stylesheet",
                 href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                 integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                 crossorigin="anonymous"),
            Title()("Hello, world!")
       )
body = Body()(
            H1()("Hello, world!"),
            Comment(" Optional JavaScript "),
            Comment(" jQuery first, then Popper.js, then Bootstrap JS "),
            Script(src="https://code.jquery.com/jquery-3.3.1.slim.min.js",
                   integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
                   crossorigin="anonymous"),
            Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
                   integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
                   crossorigin="anonymous"),
            Script(src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
                   integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
                   crossorigin="anonymous")
       )
page += head
page += body

# page.render(pretty=True)