---
layout: default
title: Getting Started
permalink: /getting_started/
---

## Installation

```shell
pip3 install tem-py
```

If you want the latest unreleased version, clone TemPy from GitHub:

```shell
git clone https://github.com/Hrabal/TemPy.git
cd TemPy
python3 setup.py install
```

<aside class="info">TemPy does not support Python 2.x. TemPy requires Python >= 3.3 to work.</aside>

TemPy is available on PyPi, so you can pip it. [PyPi.org](https://pypi.org/project/tem-py/)

If you want to customize TemPy you can clone the main [GitHub repo](https://github.com/Hrabal/TemPy).

Now that you have TemPy, just import and use some tags:

```python
from tempy.tags import Div, A
```

## Compatibility

**Python >= 3 is a must**, there is no intention to backport this project to Python 2.7.

**Python >= 3.3 is also needed**, for TemPy uses the delegation to subgenerator (the `yield from` statement) proposed in [PEP 380](https://www.python.org/dev/peps/pep-0380/).

This form of yielding is used for speed and can be easily removed if you plan to use TemPy in Python 3.0 to 3.2.x , you'll just need to substitute the `yield from` with a loop on the inner generator yielding single values.


**Python >= 3.6 is preferred**, some useful features depends on the preserved order of kwargs proposed in [PEP 468](https://www.python.org/dev/peps/pep-0468/).

The feature enabled by using TemPy with Python >= 3.6 is the ability to have named child tags in the correct order. Naming child tags is possible in Python < 3.6, but the tag's order will probably not be correct.

<aside class="success"><b>It is highly recommended to use TemPy with Python >= 3.6.</b></aside>
