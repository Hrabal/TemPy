# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Base class for rendering"""
from html import escape
from numbers import Number
from functools import partial

from .bases import TempyClass
from .tempyrepr import TempyPlace, TempyREPR


class DOMRenderer(TempyClass):

	def __repr__(self):
		return "<%s.%s %s.%s%s%s>" % (
			self.__module__,
			type(self).__name__,
			id(self),
			" Son of %s." % type(self.parent).__name__ if self.parent else "",
			" %d childs." % len(self.childs) if self.childs else "",
			" Named %s" % self._name if self._name else "",
		)

	def _render_tempy_repr(self, tempy_repr_cls, child, pretty=False):
		class Patched(tempy_repr_cls, self.__class__):
			def __init__(s, obj, *args, **kwargs):
				# Forced adoption of the patched element as son of us
				s.parent = self
				# MRO would init only the tempyREPR_cls, we force DOMElement init too
				self.__class__.__init__(s, **kwargs)
				super().__init__(obj)

		return Patched(child).render(pretty=pretty)

	def _iter_child_renders(self, pretty=False):
		for child in self.childs:
			if isinstance(child, str):
				yield escape(child)
			elif isinstance(child, Number):
				yield str(child)
			elif child.__class__.__name__ == "Escaped":
				yield child.render
			elif issubclass(child.__class__, TempyClass):
				yield child.render(pretty=pretty)
			elif not issubclass(child.__class__, TempyClass):
				tempy_repr_cls = self._search_for_view(child)
				if tempy_repr_cls:
					yield self._render_tempy_repr(tempy_repr_cls, child, pretty=pretty)
				else:
					yield escape(str(child))

	@staticmethod
	def _filter_classes(cls_list, cls_type):
		"""Filters a list of classes and yields TempyREPR subclasses"""
		for cls in cls_list:
			if isinstance(cls, type) and issubclass(cls, cls_type):
				if cls_type == TempyPlace and cls._base_place:
					pass
				else:
					yield cls

	def _evaluate_tempy_repr(self, child, repr_cls):
		"""Assign a score ito a TempyRepr class.
		The scores depends on the current scope and position of the object in which the TempyREPR is found."""
		score = 0
		if repr_cls.__name__ == self.__class__.__name__:
			# One point if the REPR have the same name of the container
			score += 1
		elif repr_cls.__name__ == self.root.__class__.__name__:
			# One point if the REPR have the same name of the Tempy tree root
			score += 1

		# Add points defined in scorers methods of used TempyPlaces
		for parent_cls in self._filter_classes(repr_cls.__mro__[1:], TempyPlace):
			for scorer in (
					method for method in dir(parent_cls) if method.startswith("_reprscore")
			):
				score += getattr(parent_cls, scorer, lambda *args: 0)(
					parent_cls, self, child
				)
		return score

	def _search_for_view(self, obj):
		"""Searches for TempyREPR class declarations in the child's class.
		If at least one TempyREPR is found, it uses the best one to make a Tempy object.
		Otherwise the original object is returned.
		"""
		evaluator = partial(self._evaluate_tempy_repr, obj)
		sorted_reprs = sorted(
			self._filter_classes(obj.__class__.__dict__.values(), TempyREPR),
			key=evaluator,
			reverse=True,
		)
		if sorted_reprs:
			# If we find some TempyREPR, we return the one with the best score.
			return sorted_reprs[0]
		return None

	def render(self, *args, **kwargs):
		"""Placeholder for subclass implementation"""
		raise NotImplementedError

	def render_childs(self, pretty=False):
		"""Public api to render all the childs using Tempy rules"""
		return "".join(self._iter_child_renders(pretty=pretty))

	def render_attrs(self):
		"""Renders the tag's attributes using the formats and performing special attributes name substitution."""
		ret = []
		for k, v in self.attrs.items():
			if v:
				if v is bool:
					ret.append(" %s" % self._SPECIAL_ATTRS.get(k, k))
				else:
					fnc = self._FORMAT_ATTRS.get(k, None)
					ret.append(' %s="%s"' % (self._SPECIAL_ATTRS.get(k, k), fnc(v) if fnc else v))
		return "".join(ret)


class CodeRenderer(TempyClass):
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

	def to_code_attrs(self):
		def formatter(k, v):
			k_norm = twist_specials.get(k, k)
			if k in self._SET_VALUES_ATTRS:
				return '%s="%s"' % (k_norm, ", ".join(map(str, v)))
			if isinstance(v, bool) or v is bool:
				return '%s="%s"' % (k_norm, "True")
			if isinstance(v, str):
				return '%s="""%s"""' % (k_norm, v)
			return "%s=%s" % (k_norm, v)

		twist_specials = {v: k for k, v in self._SPECIAL_ATTRS.items()}
		return ", ".join(formatter(k, v) for k, v in self.attrs.items() if v)


class TempyRenderer(CodeRenderer, DOMRenderer):
	pass
