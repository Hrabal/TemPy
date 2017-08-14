# TemPy
[![Build Status](https://travis-ci.org/Hrabal/TemPy.svg?branch=master)](https://travis-ci.org/Hrabal/TemPy) 
![TemPy Logo](tempy.png)

### Fast Object-Oriented HTML templating With Python!

### What
Build HTML without writing a single tag.
TemPy dynamically generates HTML and accesses it in a pure Python or jQuery fashion. Navigating the DOM and manipulating tags is also possible in a Python or jQuery-similar sintax.

### Why?
HTML is like SQL: we all use it, we know it works, we all recognize it's important, but our biggest dream is to never write a single line of it again. For SQL we have ORM's, but we're not there yet for HTML.
Templating systems are cool (Python syntax in html code) but not cool enough (you still have to write html somehow)..
..so the idea of TemPy.

### Weeeeeeee!
No parsing and a simple structure makes TemPy fast. TemPy simply adds html tags around your data, and the actual html string exists only at render time.
See below for benchmarks against other templating engines.

**Build, manipulate, and navigate HTML documents. With no HTML involved.**
