from tempy.tags import *
from tempy.elements import Css

animationCSS = Css(
    {
        "@keyframes bounce": {
            "0%": {
                "background-color": "blue;"
            },
            "25%": {
                "background-color": "red;",
                "transform": "translateX(600px);",
                "border-radius": "100%;"
                
            },
            "50%": {
                "background-color": "red;",
                "transform": "translate(600px, 600px);",
                "border-radius": "0%;"
            },
            "75%": {
                "background-color": "red;",
                "transform": "translateY(600px);",
                "border-radius": "100%;"
            },
            "100%": {
                "background-color": "green;"
            }
        },
        ".animation": {
         "width": "100px;",
         "height": "100px;",   
         "animation": "bounce;",
         "animation-duration": "4s;",
         "animation-iteration-count": "infinite;"
        }
    }
)

'''
        @keyframes bounce {
            0% {
                background-color: blue;
            }
            25%{
                background-color: red;
                transform: translateX(600px);
                border-radius: 100%;
                
            }
            50%{
                background-color: red;
                transform: translate(600px, 600px);
                border-radius: 0%;
            }
            75%{
                background-color: red;
                transform: translateY(600px);
                border-radius: 100%;
            }
            100%{
                background-color: green;
            }
        }
        .animation{
        background-color: blue;
         width: 100px;
         height: 100px;   
         animation: bounce;
         animation-duration: 4s;
         animation-iteration-count: infinite;
    }

This is the output
'''


animationDiv = Div(klass="animation")
text = Text("This is animation demo")
page = Html()(
    Head(
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0")
    ),
    Body()(
        text,
        animationDiv
    )
)


# page.render()
