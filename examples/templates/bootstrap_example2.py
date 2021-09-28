#https://startbootstrap.com/theme/coming-soon
#License : MIT license
from re import I
from tempy.tags import *

metas=[["","utf-8"],["viewport","width=device-width, initial-scale=1, shrink-to-fit=no"],["description" ,""],["author",""]]
links=[["preconnect","https://fonts.gstatic.com"],["stylesheet","https://fonts.googleapis.com/css2?family=Tinos:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap"],["stylesheet","static/styles.css"],["stylesheet","https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&amp;display=swap"]]
comment_blocks=[["SB Forms Contact Form ","This form is pre-integrated with SB Forms.","https://startbootstrap.com/solution/contact-forms","to get an API token!"],["Submit success message","This is what your users will see when the form","has successfully submitted"],["Submit error message","This is what your users will see when there is","an error submitting the form"],["Bootstrap core JS","Core theme JS","Activate your form at https://startbootstrap.com/solution/contact-forms"]]
icons=["fab fa-twitter","fab fa-facebook-f","fab fa-instagram"]
scripts=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js","static/scripts.js","https://cdn.startbootstrap.com/sb-forms-latest.js"]
page = Html(lang="en")
head=   Head()(
        Meta(charset="utf-8"),
        (Meta(name=ele[0],content=ele[1]) for ele in metas) , 
        Title()("Coming Soon - Start Bootstrap Theme"),
        Link(rel="icon", type="image/x-icon", href="static/favicon.ico"),
        Comment("Font Awesome icons (free version)"),
        Script(src="https://use.fontawesome.com/releases/v5.15.3/js/all.js", crossorigin="anonymous"),
        Comment("Google fonts"),
        (Link(rel=link[0],href=link[1])for link in links),
        Comment("Core theme CSS (includes Bootstrap)"),      
    )
body=Body()(
    Comment("Background Video"),
    Video(klass="bg-video" ,playsinline="playsinline" ,autoplay="autoplay" ,muted="muted", loop="loop")(Source().attr(src="static/bg.mp4", type="video/mp4")),
    Comment("Masthead"),
    Div(klass="masthead")(
        Div(klass="masthead-content text-white")(
            Div(klass="container-fluid px-4 px-lg-0")(
                H1(klass="fst-italic lh-1 mb-4")("Our Website is Coming Soon"),
                P(klass="mb-5")("We're working hard to finish the development of this site. Sign up below to receive updates and to be notified when we launch!"),
                (Comment(comment)for comment in comment_blocks[0]),
                Form(id="contactForm", token="API_TOKEN")(
                    Comment("Email address input"),
                    Div(klass="row input-group-newsletter")(
                        Div(klass="col")(Input (klass="form-control", id="email" ,type="email", placeholder="Enter email address..." ,label="Enter email address..." ,required="True")),
                        Div(klass="col-auto")(Button(klass="btn btn-primary disabled" ,id="submitButton" ,type="submit")("Notify Me!")),
                    ),
                    ((Div(klass="invalid-feedback mt-2",feedback=div[0])(div[1]))for div in [["email:required","An email is required."],["email:email","Email is not valid."]]),
                    (Comment(comment)for comment in comment_blocks[1]),
                    Div(klass="d-none" ,id="submitSuccessMessage")(
                        Div(klass="text-center mb-3 mt-2")(
                            Div(klass="fw-bolder")("Form submission successful!"),
                            "To activate this form, sign up at",
                            Br(),
                            A(href="https://startbootstrap.com/solution/contact-forms")("https://startbootstrap.com/solution/contact-forms"),
                        )
                    ),
                    (Comment(comment)for comment in comment_blocks[2]),
                    Div(klass="d-none" ,id="submitErrorMessage")(
                        Div(klass="text-center text-danger mb-3 mt-2")("Error sending message!")
                    )
                ),
            )
        )
    ),
    Comment("Social Icons"),
    Comment("For more icon options, visit https://fontawesome.com/icons?d=gallery&p=2&s=brands"),
    Div(klass="social-icons")(
        Div(klass="d-flex flex-row flex-lg-column justify-content-center align-items-center h-100 mt-3 mt-lg-0")(
            (A(klass="btn btn-dark m-3", href="#!")(I(klass=icon))for icon in icons),
        )
    ),
    Comment("Bootstrap core JS"),
    Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"),
    Comment("Core theme JS"),
    Script(src="static/scripts.js"),
    Comment("Activate your form at https://startbootstrap.com/solution/contact-forms"),
    Script(src="https://cdn.startbootstrap.com/sb-forms-latest.js"),
)
page+=head
page+=body
print(page.render(pretty=True))