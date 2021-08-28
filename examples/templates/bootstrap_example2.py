from re import I
from tempy.tags import *
page = Html(lang="en")
head=   Head()(
        Meta(charset="utf-8"),
        Meta(name="viewport",content="width=device-width, initial-scale=1, shrink-to-fit=no"),
        Meta(name="description" ,content=""),
        Meta(name="author",content=""),
        Title()("Coming Soon - Start Bootstrap Theme"),
        Link(rel="icon", type="image/x-icon", href="static/favicon.ico"),
        Comment("Font Awesome icons (free version)"),
        Script(src="https://use.fontawesome.com/releases/v5.15.3/js/all.js", crossorigin="anonymous"),
        Comment("Google fonts"),
        Link(rel="preconnect", href="https://fonts.gstatic.com"),
        Link(href="https://fonts.googleapis.com/css2?family=Tinos:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap", rel="stylesheet" ),
        Link(href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&amp;display=swap", rel="stylesheet"),
        Comment("Core theme CSS (includes Bootstrap)"),
        Link(href="static/styles.css" ,rel="stylesheet")
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
                Comment("SB Forms Contact Form "),
                Comment("This form is pre-integrated with SB Forms."),
                Comment("To make this form functional, sign up at"),
                Comment("https://startbootstrap.com/solution/contact-forms"),
                Comment("to get an API token!"),
                Form(id="contactForm", token="API_TOKEN")(
                    Comment("Email address input"),
                    Div(klass="row input-group-newsletter")(
                        Div(klass="col")(Input (klass="form-control", id="email" ,type="email", placeholder="Enter email address..." ,label="Enter email address..." ,required="True")),
                        Div(klass="col-auto")(Button(klass="btn btn-primary disabled" ,id="submitButton" ,type="submit")("Notify Me!")),
                    ),
                    Div(klass="invalid-feedback mt-2" ,feedback="email:required")("An email is required."),
                    Div(klass="invalid-feedback mt-2" ,feedback="email:email")("Email is not valid."),
                    Comment("Submit success message"),
                    Comment("This is what your users will see when the form"),
                    Comment("has successfully submitted"),
                    Div(klass="d-none" ,id="submitSuccessMessage")(
                        Div(klass="text-center mb-3 mt-2")(
                            Div(klass="fw-bolder")("Form submission successful!"),
                            "To activate this form, sign up at",
                            Br(),
                            A(href="https://startbootstrap.com/solution/contact-forms")("https://startbootstrap.com/solution/contact-forms"),
                        )
                    ),
                    Comment("Submit error message"),
                    Comment("This is what your users will see when there is"),
                    Comment("an error submitting the form"),
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
            A(klass="btn btn-dark m-3", href="#!")(I(klass="fab fa-twitter")),
            A(klass="btn btn-dark m-3", href="#!")(I(klass="fab fa-facebook-f")),
            A(klass="btn btn-dark m-3", href="#!")(I(klass="fab fa-instagram"))
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


