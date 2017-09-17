from .tags import *
from .tempy import Content, Css, render_template, TagAttrs, TempyREPR

__version__ = '0.5'
VERSION = tuple(map(int, __version__.split('.')))
