# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Places used by Tempy to choose the right TempyREPR to use.
Magically created starting from the tags module.
"""
import importlib
from .tempy import TempyPlace

# We create a 'Inside<>' for every tag defined in the tags.py module
all_tags = importlib.import_module('.tags', package='tempy')
for tag in dir(all_tags):
    if not tag.startswith('__'):
        inside_tag_name = 'Inside%s' % tag
        inside_cls = type(inside_tag_name, (TempyPlace, ), {})
        inside_cls.parent = getattr(all_tags, tag)
        # We put the new dynamically created class inside locals to make it avaiable from the outside
        locals()[inside_tag_name] = inside_cls
