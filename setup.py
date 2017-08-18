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

setup(name='tem-py',
      version='0.1',
      author='Federico Cerchiari',
      author_email='federicocerchiari@gmail.com',
      description='Python OOP Templating System',
      license='LICENSE',
      packages=['tempy'],
      url='https://hrabal.github.io/TemPy/',
      keywords=['python3', 'templating', 'html', 'web'],
      download_url='https://github.com/Hrabal/TemPy/archive/0.1.tar.gz',
      python_requires='>=3.3',
      )
