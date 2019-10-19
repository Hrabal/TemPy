# -*- coding: utf-8 -*-

from tempy.tags import *

# Place a video in the folder ./static to display

page = Html()(
    Head()(
        Title()(
            'Tempy - Video Tag Example'
            )
        ),
    body=Body()(
        H1()("This is an example for using video element."),
        Br(),
        Video("autoplay muted").attr(width="320", height="240", controls="True")(
            Source().attr(src="./static/movie.mp4", type="video/mp4"),
            Source().attr(src="./static/movie.obb", type="video/obb"),
        )
        )
    )