# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Utility base Classes"""


class TempyClass:
	_FORMAT_ATTRS = {
		"style": lambda x: " ".join("%s: %s;" % (k, v) for k, v in x.items()),
		"klass": " ".join,
		"comment": lambda x: x,
	}
	_SPECIAL_ATTRS = {"klass": "class", "typ": "type", "_for": "for", "_async": "async"}
	_TO_SPECIALS = {v: k for k, v in _SPECIAL_ATTRS.items()}
	_MAPPING_ATTRS = ("style",)
	_SET_VALUES_ATTRS = ("klass",)

	def __init__(self, **kwargs):
		self.parent = None
		self.childs = []
		self._name = None
		self.root = None
		self.attrs = {}
		self._depth = 0
		self._from_factory = False
		self._own_index = 0
		self.content_data = kwargs
