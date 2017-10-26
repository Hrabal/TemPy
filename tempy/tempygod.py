from .tempy import Tag
class TempyGod:
    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return type(attr, (Tag, ), {'_%s__tag' % attr: attr.lower()})

T = TempyGod()
