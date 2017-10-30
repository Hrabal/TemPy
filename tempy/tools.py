# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Tools for Tempy
"""
import sys
import importlib


def render_template(template_name, start_directory=None, **kwargs):
    if start_directory:
        sys.path.append(start_directory)
    template_module = importlib.import_module('templates.%s' % template_name)
    template = template_module.template.inject(**kwargs)
    return template.render()


class AdjustableList(list):
    def ljust(self, n, fillvalue=''):
        return self + [fillvalue] * (n - len(self))
