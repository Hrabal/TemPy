# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Base class for rendering"""
from html import escape
from numbers import Number

from .bases import TempyClass


class DOMRenderer:
	def __repr__(self):
		return "<%s.%s %s.%s%s%s>" % (
			self.__module__,
			type(self).__name__,
			id(self),
			" Son of %s." % type(self.parent).__name__ if self.parent else "",
			" %d childs." % len(self.childs) if self.childs else "",
			" Named %s" % self._name if self._name else "",
		)

	def _iter_child_renders(self, pretty=False):
		for child in self.childs:
			if isinstance(child, str):
				yield escape(child)
			elif isinstance(child, Number):
				yield str(child)
			elif issubclass(child.__class__, TempyClass):
				if child.__class__.__name__ == "Escaped":
					yield child._render
				else:
					yield child.render(pretty=pretty)
			elif not issubclass(child.__class__, TempyClass):
				tempyREPR_cls = self._search_for_view(child)
				if tempyREPR_cls:
					# If there is a TempyREPR class defined in the child class we make a DOMElement out of it
					# this abomination is used to avoid circular imports
					class Patched(tempyREPR_cls, self.__class__):
						def __init__(s, obj, *args, **kwargs):
							# Forced adoption of the patched element as son of us
							s.parent = self
							# MRO would init only the tempyREPR_cls, we force DOMElement init too
							self.__class__.__init__(s, **kwargs)
							super().__init__(obj)

					yield Patched(child).render(pretty=pretty)
				else:
					yield escape(str(child))

	def render(self, *args, **kwargs):
		"""Placeholder for subclass implementation"""
		raise NotImplementedError

	def render_childs(self, pretty=False):
		"""Public api to render all the childs using Tempy rules"""
		return "".join(self._iter_child_renders(pretty=pretty))


class CodeRenderer:
	def to_code(self, pretty=False):
		ret = []
		prettying = "\n" + ("\t" * self._depth) if pretty else ""
		childs_to_code = []
		for child in self.childs:
			if issubclass(child.__class__, TempyClass):
				child_code = child.to_code(pretty=pretty)
				childs_to_code.append(child_code)
			else:
				childs_to_code.append('"""%s"""' % child)

		childs_code = ""
		if childs_to_code:
			childs_code = "(%s%s%s)" % (prettying, ", ".join(childs_to_code), prettying)
		class_code = ""
		if self._from_factory:
			class_code += "T."
			if getattr(self, "_void", False):
				class_code += "Void."
		class_code += self.__class__.__name__
		ret.append("%s(%s)%s" % (class_code, self.to_code_attrs(), childs_code))
		return "".join(ret)
