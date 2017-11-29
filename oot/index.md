---
layout: default
title: Object-Oriented Templating
permalink: /oot/
---

# OOT - Object Oriented Templating

## Template Objects

TemPy is designed to provide Object Oriented Templating. You can subclass TemPy classes and define their inner tree structure, and also add custom methods.
Tempy classes can be subclassed as any other Python class, TemPy will use a `init` (no double underscore) method to correctly handle the hierarchy.


## TemPy Repr's add an html repr to your objects

Another way OOT is intended is through the `TempyREPR` classes. Those can be defined as nested classes inside your own non-TemPy class, place your instances inside the DOM, and TemPy will use them when rendering the DOM.
