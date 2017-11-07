## Tempy | Contibution program and guidelines

### Guidelines
Any contribution is welcome, fork and PR if you have some ideas you want to code or you found a bug, I'll check them out.

Please write tests for your new proposed features and run already written tests for any contribution you make.
Test are important, no merge will be made without some test coverage. If you don't know how to write/run tests ask (Tempy tests are written with [Unittest](https://docs.python.org/3/library/unittest.html) )

Contact me if you want to help maintaining this project or if you are willing to suggest ideas.

Open an Issue to ask for features, develop some of the next goals, or report a bug.

I have a [Slack](https://tempy-dev.slack.com) for TemPy dev discussions (ask for an invitation at federicocerchiari @ gmail . com).

### TODO plan:
Planned evolution of this project:
- [ ] `stable` concept refactor... there should be a better way!
- [ ] New class: `CssManager` (or something like that) that extracts common style properties from a formed DOM, creates the `Css` instance and adds it in the `<head>`. Extra feature: dumps the css to a versioned file in the static folder and adds a link to this file in the page.
- [x] Better exception handling.
- [x] Manage Tempy object subclassing to use a custom object as a renderable for businnes logic item (i.e: SQLAlchemy's declarative with a Tempy template in it that can be rendered at ease)
- [x] TemPy widgets, see the widget branch.
- [x] Better pretty formatting.
- [x] Writing more tests.

see [open issues](https://github.com/Hrabal/TemPy/issues) for a complete list of contribution opportunities.

Ideas I'm thinking about:
- [x] Html to TemPy command line converter tool, accepts plain html and makes a .py tempy module.
- ~~Python 2 compatibility (maybe?).~~
- [ ] Performance: always needed, maybe a `_partial_render` method that traverse the html tree in a depth-first reverse order and "stabilize" all the leafs? Is this useful?
- [ ] Adding .find method to the T object use with css-like selectors (i.e: `Html().find('#myid')`)?
- [x] Adding a jQuery-ish god object `T` to use as a find method inside a DOMElement sublass (i.e: `T('#myid').some_tempy_method()`)?
- Cache for css builder module in a separate script (i.e: `shell >>> tempy -build_css my_template.py` outputs a css in the static folder and the `CssManager` search for that version in the statics before doing any work)?
- Any suggestion?
