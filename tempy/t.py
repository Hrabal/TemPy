# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import importlib
from html.parser import HTMLParser
from .tempy import Tag, VoidTag

class TempyParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.unknown_tag_maker = TempyFactory()
        self.tempy_tags = importlib.import_module('.tags', package='tempy')

    def _make_tempy_tag(self, tag, attrs, void):
        tempy_tag_cls = getattr(self.tempy_tags, tag.title(), None)
        if not tempy_tag_cls:
            unknow_maker = [self.unknown_tag_maker, self.unknown_tag_maker.Void][void]
            tempy_tag_cls = unknow_maker[tag]
        tempy_tag = tempy_tag_cls(**dict(attrs))
        if not self.current_tag:
            self.result.append(tempy_tag)
            if not void:
                self.current_tag = tempy_tag
        else:
            self.current_tag(tempy_tag)
            self.current_tag = self.current_tag.childs[-1]

    def handle_starttag(self, tag, attrs):
        self._make_tempy_tag(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._make_tempy_tag(tag, attrs, True)

    def handle_endtag(self, tag):
        self.current_tag = self.current_tag.parent

    def handle_data(self, data):
        self.current_tag(data)

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass


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


class TempyGod(TempyFactory):

    def __init__(self):
        super().__init__()
        self._parser = TempyParser()

    def from_string(self, html_string):
        self._parser.feed(html_string)
        return self._parser.result


T = TempyGod()
