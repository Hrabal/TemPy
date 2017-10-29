from .tools import render_template
from .elements import Tag, VoidTag, Css, Content
from .tempyrepr import TempyREPR
from .places import TempyPlace

__version__ = '0.6.0'
VERSION = tuple(map(int, __version__.split('.')))
