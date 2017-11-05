# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
from .tools import render_template
from .elements import Tag, VoidTag, Css, Content
from .tempyrepr import TempyREPR
from .places import TempyPlace
from .t import T


__version__ = '1.0.0'
VERSION = tuple(map(int, __version__.split('.')))
