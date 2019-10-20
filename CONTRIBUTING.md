# Tempy | Contibution program and guidelines

## Guidelines
Any contribution is welcome.
The TODO list below is a general plan of what I (we!) intend to do next. You can find the actual planned activities looking  in the [Issues](https://github.com/Hrabal/TemPy/issues) of this repo.

If you want to propose (or ask for) a new feature, if you want to propose a refactoring of some part of the code, or if you find a bug, please open a new issue with your idea.

Every contribution *should* have its tests and will have to pass already written tests.
Tests are important, and no merge will be made without some test coverage. If you don't know how to write/run tests just AMA on our  [Slack](https://tempy-dev.slack.com) channel. 
Tempy tests are written with [Unittest](https://docs.python.org/3/library/unittest.html), every PR you make will be analyzed by [Travis CI](https://travis-ci.org/Hrabal/TemPy).

Contact me if you want to help to maintain this project or if you are willing to suggest ideas.
We have a [Slack](https://tempy-dev.slack.com) for TemPy dev discussions (ask for an invitation to federicocerchiari @ gmail . com).

### Code Style
This project does not have a coding style guideline (except [PEP8](https://www.python.org/dev/peps/pep-0008/) and [PEP20](https://www.python.org/dev/peps/pep-0020/) of course) , just code as you like to code!

## Workflow
Every development is tracked using Issues. If you want to work on a specific issue, ask for assignment. And if you don't find an issue for what you want to work on, open a new issue with your proposed development.

Small (2/3 commits, 1 contributor) contributions should follow this simple workflow:
- Ask to be assigned to the issue
- Fork this repo: [GitHub guide on forking](https://help.github.com/articles/fork-a-repo/)
- Do the coding on the forked repo in the master branch
- Make a Pull Request: [GitHub guide on making a PR](https://help.github.com/articles/about-pull-requests/)
Some CI and code quality services will be triggered and 5/10 mins after your PR you'll see in the PR page if your contribution is breaking some tests, if it contain some code that can be made better and if it have good test coverage.
I'll check the PR and merge, or review your code if I have suggestions on something you wrote.

Bigger developments (i.e: a new widget, a new complex feature, a deep refactor, more than one person working on the feature), etc..) will follow a different workflow:
- Discuss the development strategy on the Issue
- Discuss particular problems in the Slack channel
- I'll make a new branch dedicated to this feature with no CI
- When the feature is ready I'll perform the merge into the master branch

## TODO plan:
Planned evolution of this project:
- [ ] `stable` concept refactor... there should be a better way!
- [ ] New class: `CssManager` (or something like that) that extracts common style properties from a formed DOM, creates the `Css` instance and adds it in the `<head>`. Extra feature: dumps the css to a versioned file in the static folder and adds a link to this file in the page.
- [x] Better exception handling.
- [x] Manage Tempy object subclassing to use a custom object as a renderable for business logic item (i.e: SQLAlchemy's declarative with a Tempy template in it that can be rendered at ease)
- [x] TemPy widgets, see the widget branch.
- [x] Better pretty formatting.
- [x] Writing more tests.

See [open issues](https://github.com/Hrabal/TemPy/issues) for a complete list of contribution opportunities.

Ideas I'm thinking about:
- [x] Html to TemPy command line converter tool, accepts plain html and makes a .py tempy module.
- ~~Python 2 compatibility (maybe?).~~
- [ ] Performance: always needed, maybe a `_partial_render` method that traverses the html tree in a depth-first reverse order and "stabilizes" all the leafs? Is this useful?
- [ ] Adding .find method to the T object use with css-like selectors (i.e: `Html().find('#myid')`)?
- [x] Adding a jQuery-ish god object `T` to use as a find method inside a DOMElement sublass (i.e: `T('#myid').some_tempy_method()`)?
- Cache for css builder module in a separate script (i.e: `shell >>> tempy -build_css my_template.py` outputs a css in the static folder and the `CssManager` search for that version in the statics before doing any work)?
- Any suggestions?
