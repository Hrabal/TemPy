# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Elemnts used inside Tempy Classes
"""
import re
from copy import copy
from types import GeneratorType
from collections import Mapping, Iterable, ChainMap

from .tempy import DOMElement
from .exceptions import WrongArgsError, WrongContentError, ContentError, TagError, AttrNotFoundError
import inspect


class TagAttrs(dict):
    """
    Html tag attributes container, a subclass of dict with __setitiem__ and update overload.
    Manages the manipulation and render of tag attributes, using the dict api, with few exceptions:
    - space separated multiple value keys
        i.e. the class atrribute, an update on this key will add the value to the list
    - mapping type attributes
        i.e. style attribute, an udpate will trigger the dict.update method

    TagAttrs.render formats all the attributes in the proper html format.
    """
    _MAPPING_ATTRS = ('style',)
    _SET_VALUES_ATTRS = ('klass',)
    _SPECIALS = {
        'klass': 'class',
        'typ': 'type',
        '_for': 'for',
        '_async': 'async',
    }
    _TO_SPECIALS = {v: k for k, v in _SPECIALS.items()}
    _FORMAT = {
        'style': lambda x: ' '.join('%s: %s;' % (k, v) for k, v in x.items()),
        'klass': ' '.join,
        'comment': lambda x: x
    }

    def __init__(self, *args, **kwargs):
        super().__setitem__('klass', set())
        super().__setitem__('style', {})
        super().__init__(**kwargs)
        if not args:
            pass
        else:
            for arg in args:
                if not isinstance(arg, str):
                    raise WrongArgsError(self, arg, 'Positional arguments should be strings.')
            for boolean_key in args:
                super().__setitem__(boolean_key, bool)

    def __setitem__(self, key, value):
        if key in self._SET_VALUES_ATTRS:
            for v in value.split():
                self[key].add(v)
        elif key in self._MAPPING_ATTRS:
            if isinstance(value, str):
                splitted = iter(re.split(';|:', value))
                value = dict(zip(splitted, splitted))
            self[key].update(value)
        else:
            super().__setitem__(key, value)

    def __copy__(self):
        return TagAttrs(**self)

    def update(self, attrs=None, **kwargs):
        if attrs is not None:
            for k, v in attrs.items() if isinstance(attrs, Mapping) else attrs:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def render(self):
        """Renders the tag's attributes using the formats and performing special attributes name substitution."""
        ret = []
        for k, v in self.items():
            if v:
                f_string = (' {}="{}"', ' {}')[v is bool]
                f_args = (self._SPECIALS.get(k, k), self._FORMAT.get(k, lambda x: x)(v))[:2 + (v is bool)]
                ret.append(f_string.format(*f_args))
        return ''.join(ret)

    def to_code(self):
        def formatter(k, v):
            k_norm = twist_specials.get(k, k)
            if k in self._SET_VALUES_ATTRS:
                return '%s="%s"' % (k_norm, ', '.join(map(str, v)))
            if isinstance(v, bool) or v is bool:
                return '%s="%s"' % (k_norm, 'True')
            if isinstance(v, str):
                return '%s="""%s"""' % (k_norm, v)
            return '%s=%s' % (k_norm, v)

        twist_specials = {v: k for k, v in self._SPECIALS.items()}
        return ', '.join(formatter(k, v) for k, v in self.items() if v)


class Tag(DOMElement):
    """
    Provides an api for tag inner manipulation and for rendering.
    """
    _template = '{pretty}<{tag}{attrs}>{inner}{pretty}</{tag}>'
    _void = False

    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', {})
        self.attrs = TagAttrs()
        if args:
            self.attr(*args)
        if kwargs:
            self.attr(**kwargs)
        super().__init__(**data)
        self._tab_count = 0
        self._render = None
        if self._void:
            self._render = self.render()

    def _get__tag(self):
        for cls in self.__class__.__mro__:
            try:
                return getattr(self, '_%s__tag' % cls.__name__)
            except AttributeError:
                pass
        raise TagError(self, '_*__tag not defined for this class or bases.')

    def __repr__(self):
        css_repr = '%s%s' % (
            ' .css_class (%s)' % (self.attrs['class']) if self.attrs.get('class', None) else '',
            ' .css_id (%s)' % (self.attrs['id']) if self.attrs.get('id', None) else '',
        )
        return super().__repr__()[:-1] + '%s>' % css_repr

    def __copy__(self):
        new = super().__copy__()
        new.attrs = copy(self.attrs)
        return new

    def attr(self, *args, **kwargs):
        """Add an attribute to the element"""
        for arg in args:
            if not isinstance(arg, str):
                raise WrongArgsError(self, arg, 'Positional arguments should be strings.')
        self._stable = False
        kwargs.update({k: bool for k in args})
        self.attrs.update(kwargs)
        return self

    def remove_attr(self, attr):
        """Removes an attribute."""
        self._stable = False
        self.attrs.pop(attr, None)
        return self

    def set_id(self, css_id):
        self.attrs['id'] = css_id
        return self

    def id(self):
        """Returns the tag css id"""
        return self.attrs.get('id', None)

    def is_id(self, css_id):
        """Check if tag have the given id"""
        return css_id == self.id()

    def has_class(self, csscl):
        """Checks if this element have the given css class."""
        return csscl in self.attrs['klass']

    def toggle_class(self, csscl):
        """Same as jQuery's toggleClass function. It toggles the css class on this element."""
        self._stable = False
        action = ('add', 'remove')[self.has_class(csscl)]
        return getattr(self.attrs['klass'], action)(csscl)

    def add_class(self, cssclass):
        """Adds a css class to this element."""
        if self.has_class(cssclass):
            return self
        return self.toggle_class(cssclass)

    def remove_class(self, cssclass):
        """Removes the given class from this element."""
        if not self.has_class(cssclass):
            return self
        return self.toggle_class(cssclass)

    def css(self, *props, **kwprops):
        """Adds css properties to this element."""
        self._stable = False
        styles = {}
        if props:
            if len(props) == 1 and isinstance(props[0], Mapping):
                styles = props[0]
            else:
                raise WrongContentError(self, props, 'Arguments not valid')
        elif kwprops:
            styles = kwprops
        else:
            raise WrongContentError(self, None, 'args OR wkargs are needed')
        return self.attr(style=styles)

    def hide(self):
        """Adds the "display: none" style attribute."""
        self._stable = False
        self.attrs['style']['display'] = 'none'
        return self

    def show(self, display=None):
        """Removes the display style attribute.
        If a display type is provided """
        self._stable = False
        if not display:
            self.attrs['style'].pop('display')
        else:
            self.attrs['style']['display'] = display
        return self

    def toggle(self):
        """Same as jQuery's toggle, toggles the display attribute of this element."""
        self._stable = False
        return self.show() if self.attrs['style']['display'] == 'none' else self.hide()

    def html(self, pretty=False):
        """Renders the inner html of this element."""
        return self.render_childs(pretty=pretty)

    def text(self):
        """Renders the contents inside this element, without html tags."""
        texts = []
        for child in self.childs:
            if isinstance(child, Tag):
                texts.append(child.text())
            elif isinstance(child, Content):
                texts.append(child.render())
            else:
                texts.append(child)
        return ' '.join(texts)

    def render(self, *args, **kwargs):
        """Renders the element and all his childrens."""
        # args kwargs API provided for last minute content injection
        #self._reverse_mro_func('pre_render')
        pretty = kwargs.pop('pretty', False)
        for arg in args:
            if isinstance(arg, dict):
                self.inject(arg)
        if kwargs:
            self.inject(kwargs)

        # If the tag or his contents are not changed, we skip all the work
        if self._stable and self._render:
            return self._render

        tag_data = {
            'tag': self._get__tag(),
            'attrs': self.attrs.render(),
            'pretty': '\n' + ('\t' * self._depth) if pretty else '',
        }
        tag_data['inner'] = self.render_childs(pretty) if not self._void and self.childs else ''

        # We declare the tag is stable and have an official render:
        self._render = self._template.format(**tag_data)
        self._stable = True
        return self._render

    def apply_function(self, format_function):
        gen = ((index, child) for index, child in enumerate(self.childs) if child is not None)
        for (index, child) in gen:
            if isinstance(child, Tag):
                child.apply_function(format_function)
            elif isinstance(child, Content):
                child.apply_function(format_function)
            else:
                self.childs[index] = format_function(self.childs[index])


class VoidTag(Tag):
    """
    A void tag, as described in W3C reference: https://www.w3.org/TR/html51/syntax.html#void-elements
    """
    _void = True
    _template = '<{tag}{attrs}/>'


class Css(Tag):
    """Special class for the style tag.
    Css attributes can be altered with the Css.update method. At render time the attr dict is transformed in valid css:
    Css({'html': {
            'body': {
                'color': 'red',
                'div': {
                    'color': 'green',
                    'border': '1px'
                }
            }
        },
        '#myid': {'color': 'blue'}
    })
    translates to:
    <style>
    html body {
        color: red;
    }

    html body div {
        color: green;
        border: 1px;
    }
    #myid {
        'color': 'blue';
    }
    </style>
    """
    _template = '<style>{css}</style>'

    def __init__(self, *args, **kwargs):
        css_styles = self._parse__args(*args, **kwargs)
        super().__init__(css_attrs=css_styles)

    def _parse__args(self, *args, **kwargs):
        css_styles = {}
        if args:
            if len(args) > 1:
                raise WrongContentError(self, args, 'Css accepts max one positional argument.')
            if isinstance(args[0], dict):
                css_styles.update(args[0])
            elif isinstance(args[0], Iterable):
                if any(map(lambda x: not isinstance(x, dict), args[0])):
                    raise WrongContentError(self, args, 'Unexpected arguments.')
                css_styles = dict(ChainMap(*args[0]))
        css_styles.update(kwargs)
        return css_styles

    def update(self, *args, **kwargs):
        css_styles = self._parse__args(*args, **kwargs)
        self.attrs['css_attrs'].update(css_styles)

    @staticmethod
    def render_dom_element_to_css(element):
        if 'id' in element.attrs:
            return '#' + element.attrs['id']
        if 'klass' in element.attrs and element.attrs['klass']:
            return '.' + '.'.join(element.attrs['klass'])
        element.attrs['id'] = id(element)
        return '#' + str(id(element))

    def render(self, *args, **kwargs):
        pretty = kwargs.pop('pretty', False)
        result = []
        nodes_to_parse = [([], self.attrs['css_attrs'])]

        while nodes_to_parse:
            parents, node = nodes_to_parse.pop(0)
            gen = [parent for parent in parents] if parents else []
            for parent in gen:
                if isinstance(parent, tuple):
                    result.append(', '.join(parent))
                elif inspect.isclass(parent):
                    result.append(getattr(parent, "_" + parent.__name__ + "__tag") + " ")
                elif isinstance(parent, DOMElement):
                    result.append(self.__class__.render_dom_element_to_css(parent) + " ")
                else:
                    result.append("%s " % parent)
            result.append('{ ')

            for key, value in node.items():
                if isinstance(value, str):
                    result.append('%s: %s; %s' % (key, value, "\n" if pretty else ""))
                elif hasattr(value, '__call__'):
                    result.append('%s: %s; %s' % (key, value(), "\n" if pretty else ""))
                elif isinstance(value, dict):
                    nodes_to_parse.append(([p for p in parents] + [key], value))
            if result:
                result.append("} " + ("\n\n" if pretty else ""))
        return self._template.format(css=''.join(result))

    def dump(self, filename, **kwargs):
        with open(filename, 'w') as file_to_write:
            self._template = '{css}'
            file_to_write.write(self.render(**kwargs))
            self._template = '<style>{css}</style>'

    def replace_element(self, selector_list, new_style, ignore_error=True):
        if new_style is None or not isinstance(new_style, (str, dict)) or not new_style:
            if ignore_error:
                return
            else:
                raise WrongArgsError(self, new_style, 'Second argument should be a non-empty string or dictionary.')

        try:
            element_node = self.find_attr(selector_list)
        except (AttrNotFoundError, WrongArgsError) as wrong_args_error:
            if ignore_error:
                return
            else:
                print(wrong_args_error.__repr__())
                raise

        if element_node:
            element_node[selector_list[-1]] = new_style
        elif not element_node and selector_list[0] in self.attrs['css_attrs']:
            (self.attrs['css_attrs'])[selector_list[0]] = new_style

    def find_attr(self, selector_list):
        if not isinstance(selector_list, list) or len(selector_list) < 1:
            raise WrongArgsError(self, selector_list, 'The provided argument should be a non-empty list.')

        found_node = self.attrs['css_attrs']
        parent_node = None

        for child in selector_list:
            if child in found_node:
                parent_node = found_node
                found_node = found_node[child]
            else:
                raise AttrNotFoundError(self, selector_list, 'Provided element does not exist.')
        return parent_node

    def clear(self, selector_list=None, ignore_error=True):
        if selector_list is None:
            self.attrs['css_attrs'] = {}
            return

        try:
            element_node = self.find_attr(selector_list)
        except (AttrNotFoundError, WrongArgsError) as wrong_args_error:
            if ignore_error:
                return
            else:
                print(wrong_args_error.__repr__())
                raise

        if element_node:
            element_node.pop(selector_list[-1], None)
        elif not element_node and selector_list[0] in self.attrs['css_attrs']:
            (self.attrs['css_attrs']).pop([selector_list[0]], None)


class Content(DOMElement):
    """
    Provides the ability to use a simil-tag object as content placeholder.
    At render time, a content with the same name is searched in parents, the nearest one is used.
    If no content with the same name is used, an empty string is rendered.
    If instantiated with the named attribute content, this will override all the content injection on parents.
    """

    def __init__(self, name=None, content=None, t_repr=None):
        super().__init__()
        self._tab_count = 0
        if not name and not content:
            raise ContentError(self, 'Content needs at least one argument: name or content')
        self._name = name
        self._fixed_content = content
        self._t_repr = t_repr
        if self._t_repr and not isinstance(self._t_repr, DOMElement):
            raise ContentError(self, 'template argument should be a DOMElement')
        self._stable = False

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [{
            '_name': t._name,
            'content': list(t.content),
            '_t_repr': t._t_repr,
        } for t in (self, other)]
        return comp_dicts[0] == comp_dicts[1]

    def __copy__(self):
        return self.__class__(self._name, self._fixed_content, self._t_repr)

    @property
    def content(self):
        content = self._fixed_content
        if not content and self.parent:
            content = self.parent._find_content(self._name)
        if isinstance(content, DOMElement) or content:
            if isinstance(content, DOMElement):
                yield content
            elif isinstance(content, (list, tuple, GeneratorType)):
                yield from content
            elif isinstance(content, dict):
                yield content
            elif isinstance(content, str):
                yield content
            else:
                yield from iter([content, ])
        else:
            return

    @property
    def length(self):
        return len(list(self.content))

    def render(self, *args, **kwargs):
        pretty = kwargs.pop('pretty', False)
        ret = []
        for content in self.content:
            if content is not None:
                if isinstance(content, DOMElement):
                    ret.append(content.render(pretty=pretty))
                else:
                    if self._t_repr:
                        ret.append(self._t_repr.inject(content).render(pretty=pretty))
                    elif isinstance(content, dict):
                        for v in content.values():
                            if v is not None:
                                if isinstance(v, list):
                                    ret = ret + [str(i) for i in v if i is not None]
                                else:
                                    ret.append(str(v))
                    else:
                        ret.append(str(content))
        return ' '.join(ret)

    def apply_function(self, format_function):
        gen = ((index, content) for index, content in enumerate(self.content) if content is not None)
        for (index, content) in gen:
            if isinstance(content, DOMElement):
                content.apply_function(format_function)
            else:
                if self._t_repr:
                    if isinstance(self._t_repr, DOMElement):
                        self._t_repr.apply_function(format_function)
                    else:
                        self._t_repr = format_function(self._t_repr)
                elif isinstance(content, dict):
                    dict_gen = (key for key in content if content[key] is not None)
                    for key in dict_gen:
                        if isinstance(content[key], list):
                            content[key] = [format_function(elem) for elem in content[key] if elem is not None]
                        else:
                            content[key] = format_function(content[key])
                else:
                    self.content[index] = format_function(self.content[index])
