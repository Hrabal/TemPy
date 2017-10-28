from .tempy import Tag, VoidTag


class TempyFactory:

    def __init__(self, void_maker=False):
        self._void = void_maker
        if not self._void:
            self.Void = TempyFactory(void_maker=True)

    def make_tempy(self, tage_name):
        base_class = [Tag, VoidTag][self._void]
        return type(tage_name, (base_class, ), {'_%s__tag' % tage_name: tage_name.lower()})

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return self.make_tempy(attr)

    def __getitem__(self, key):
        tag = self.make_tempy(key)
        return tag


T = TempyFactory()
