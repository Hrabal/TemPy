# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import sys
from types import ModuleType

__version__ = '1.3.0'
VERSION = tuple(map(int, __version__.split('.')))

if sys.version_info < (3, 3):
    raise RuntimeError('You need Python >= 3.3 for this module.')


_shorcuts = {
    'render_template': 'tools',
    'Tag': 'elements',
    'VoidTag': 'elements',
    'Css': 'elements',
    'Content': 'elements',
    'TempyREPR': 'tempyrepr',
    'TempyPlace': 'tempyrepr',
    'T': 't',
    'Escaped': 'tempy',
}


class module(ModuleType):

    def __getattr__(self, name):
        if name in _shorcuts.keys():
            submodule = __import__('tempy.' + _shorcuts[name], globals(), locals(), [name, ])
            return getattr(submodule, name)
        r = ModuleType.__getattribute__(self, name)
        return r

    def __dir__(self):
        result = list(sys.modules['tempy'].__all__)
        result.extend(('__file__', '__doc__', '__all__',
                       '__docformat__', '__name__', '__path__',
                       '__package__', '__version__'))
        return result


old_module, sys.modules['tempy'] = sys.modules['tempy'], module('tempy')
sys.modules['tempy'].__dict__.update({
    '__file__': __file__,
    '__package__': 'tempy',
    '__path__': __path__,
    '__doc__': __doc__,
    '__version__': __version__,
    '__all__': tuple(_shorcuts.keys()),
    '__docformat__': 'restructuredtext en'
})
