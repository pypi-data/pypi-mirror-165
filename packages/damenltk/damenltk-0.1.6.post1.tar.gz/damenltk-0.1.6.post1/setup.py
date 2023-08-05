#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DameNLTK; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import os
import codecs
import os.path
import re
import sys
import unittest
from os import path

from setuptools import setup
from setuptools.command.test import test as TestClass

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(name='damenltk',
      url='http://github.com/davidam/damenltk',
      author='David Arroyo Menéndez',
      author_email='davidam@gnu.org',
      license='GPLv3',
      version='0.1.6.post1',
      description='Learning about Natural Language Tool Kit (NLTK) from tests',
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords="nlp nltk",
      packages=[
          'damenltk',
          'damenltk.src',
          'damenltk.test'
      ],
      data_files=[('damenltk', ['damenltk/runtest.sh'])],
      namespace_packages=[
          'damenltk',
          'damenltk.src'
      ],
      setup_requires=[
          'markdown'
      ],
      tests_require=[
          'httpretty==0.8.6'
      ],
      install_requires=[
          'markdown',
          'nltk'
      ],
      zip_safe=False)
