#!/usr/bin/env python

#   Copyright 2017 Federico Cerchiari <federicocerchiari@gmail.com>
#
#   this file is part of tempy
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from setuptools import setup

from tempy import __version__

long_description = """
Build HTML without writing a single tag.
TemPy dynamically generates HTML and accesses it in a pure Python or jQuery fashion.
Navigating the DOM and manipulating tags is also possible in a Python or jQuery-similar sintax.

No parsing and a simple structure makes TemPy fast. TemPy simply adds html tags around your data, and the actual html string exists only at render time.
"""

setup(name='tem-py',
      version=__version__,
      author='Federico Cerchiari',
      author_email='federicocerchiari@gmail.com',
      description='Python OOP Templating System',
      license='APACHE 2.0',
      packages=['tempy'],
      url='https://github.com/Hrabal/TemPy',
      keywords=['python3', 'templating', 'html', 'web'],
      download_url='https://github.com/Hrabal/TemPy/archive/%s.tar.gz' % __version__,
      python_requires='>=3.3',
      long_description=long_description
      )
