---
layout: default
title: Object-Oriented Templating
permalink: /oot/
---

# OOT - Object Oriented Templating

## Template Objects

TemPy is designed to provide Object Oriented Templating. You can subclass TemPy classes and define their inner tree structure, and also add custom methods as for normal Python classes.
Tempy classes can be subclassed as any other Python class; TemPy will use an `init` (no double underscore) method to correctly handle the hierarchy.

Making templates will let you, for instance, define a base page structure, and than subclass this into page-specific templates.

It's also useful if you have static shared html in your page, you can define those once, import and put them everywhere you need without re-writing them every time.


## TemPy Repr's add an html repr to your objects

Another way OOT is implemented is through the `TempyREPR` classes. Those can be defined as nested classes inside your own non-TemPy class: Place your instances inside the DOM, and TemPy will use them when rendering the DOM.

This way you can define models of you webapp/site and define in the same place the way they will be represented in the html page, just like `__repr__`.
