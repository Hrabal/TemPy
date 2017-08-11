## Tempy | Contibution program and guidelines

### Guidelines
Any contribution is welcomed, fork and PR if you have some ideas you want to code in, I'll check them out.
Please write your own tests, no merge will be made without the relative tests.

PM me if you want to help maintaining this project or if you are willing to develop some of the next goals.

Open an Issue to ask for features, suggest ideas, or report a bug.

### Program
Planned evolution of this project:
- Better exception handling.
- Python 2 compatibility.
- Manage Tempy object subclassing to use a custom object as a renderable for businnes logic item (i.e: SQLAlchemy's declarative with a Tempy template in it that can be rendered at ease)
- Make pretty formatting of the output html.
- Implement math operators for DOMElement (i.e: `Div() += Div()` add the latter as a child or `Div() | Div()` makes a new `Content` containint the two.)
- Writing more tests.

Ideas I'm thinking about:
- Performance: always needed, maybe a `_partial_render` method that traverse the html tree in a depth-first reverse order and "stabilize" all the leafs? Is this useful?
- Adding .find method to use with css-like selectors (i.e: `Html().find('#myid')`)?
- New class: `CssManager` extracts the style properties from content, and creates the css file with the correct selector?
- Cache for css builder module in a separate script (i.e: `shell >>> tempy -build_css my_template.py` outputs a css in the static folder and the `CssManager` search for that in the statics)?
- Any suggestion?
