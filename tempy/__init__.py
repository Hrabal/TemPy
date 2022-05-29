# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import sys
from types import ModuleType

__version__ = "1.5.3"
VERSION = tuple(map(int, __version__.split(".")))

if sys.version_info < (3, 3):
    raise RuntimeError("TemPy requires Python >= 3.3.")


_shortcuts = {
    "render_template": "tools",
    "Tag": "elements",
    "VoidTag": "elements",
    "Css": "css",
    "Content": "content",
    "TempyREPR": "tempyrepr",
    "TempyPlace": "tempyrepr",
    "T": "t",
    "Escaped": "tempy",
}


class Module(ModuleType):
    def __getattr__(self, name):
        if name in _shortcuts:
            submodule = __import__(
                "tempy." + _shortcuts[name], globals(), locals(), [name]
            )
            return getattr(submodule, name)
        r = ModuleType.__getattribute__(self, name)
        return r

    def __dir__(self):
        result = list(sys.modules["tempy"].__all__)
        result.extend(
            (
                "__file__",
                "__doc__",
                "__all__",
                "__docformat__",
                "__name__",
                "__path__",
                "__package__",
                "__version__",
            )
        )
        return result


old_module, sys.modules["tempy"] = sys.modules["tempy"], Module("tempy")
sys.modules["tempy"].__dict__.update(
    {
        "__file__": __file__,
        "__package__": "tempy",
        "__path__": __path__,
        "__doc__": __doc__,
        "__version__": __version__,
        "__all__": tuple(_shortcuts),
        "__docformat__": "restructuredtext en",
    }
)
