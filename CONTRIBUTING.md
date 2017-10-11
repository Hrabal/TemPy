## Tempy | Contibution program and guidelines

### Guidelines
Any contribution is welcomed, fork and PR if you have some ideas you want to code in, I'll check them out.

Please write tests for your new proposed features and run already written tests for any contribution you make.
Test are important, no merge will be made without a decent test coverage. If you don't know how to write/run test just ask!

PM me if you want to help maintaining this project or if you are willing to suggest ideas.

Open an Issue to ask for features, develop some of the next goals, or report a bug.

We have a [Slack](https://tempy-dev.slack.com) for TemPy dev discussions (ask for an invitation at federicocerchiari @ gmail . com).

### TODO plan:
Planned evolution of this project:
- [x] Better exception handling.
- [x] Manage Tempy object subclassing to use a custom object as a renderable for businnes logic item (i.e: SQLAlchemy's declarative with a Tempy template in it that can be rendered at ease)
- [ ] TemPy widgets, see the widget branch.
- [ ] Better pretty formatting.
- [x] Writing more tests.
- [ ] `stable` concept refactor... there should be a better way!

Ideas I'm thinking about:
- Html to TemPy command line converter tool, accepts plain html and makes a .py tempy module.
- ~~Python 2 compatibility (maybe?).~~
- Performance: always needed, maybe a `_partial_render` method that traverse the html tree in a depth-first reverse order and "stabilize" all the leafs? Is this useful?
- Adding .find method to use with css-like selectors (i.e: `Html().find('#myid')`)?
- Adding a jQuery-ish god object `T` to use as a find method inside a DOMElement sublass (i.e: `T('#myid').some_tempy_method()`)?
- New class: `CssManager` extracts common style properties from the DOM, creates the `Css` instance and adds it in the `<head>`?
- Cache for css builder module in a separate script (i.e: `shell >>> tempy -build_css my_template.py` outputs a css in the static folder and the `CssManager` search for that version in the statics before doing any work)?
- Any suggestion?
