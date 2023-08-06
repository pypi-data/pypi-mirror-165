#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2021  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gmail.com>
# Maintainer: David Arroyo Menéndez <davidam@gmail.com>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with dameformats; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import os
import re
import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(name='dameformats',
      version='0.1.3',
      description='Learning Formats from Tests by David Arroyo Menéndez',
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
      ],
      keywords='formats tests',
      url='http://github.com/davidam/dameformats',
      author='David Arroyo Menéndez',
      author_email='davidam@gmail.com',
      license='GPLv3',
      packages=['dameformats', 'dameformats.src', 'dameformats.tests', 'dameformats.files'],
      package_dir={'dameformats': 'dameformats', 'dameformats.src': 'dameformats/src', 'dameformats.tests': 'dameformats/tests', 'dameformats.files': 'dameformats/files'},
      package_data={'dameformats.tests': ['*'],
                    'dameformats.src': ['*'],
                    'dameformats.files': ['*']},
      data_files=[('dameformats', ['dameformats/runtests.sh', 'dameformats/files/exer1-interface-data.json', 'dameformats/files/partial.csv', 'dameformats/files/min.csv', 'dameformats/files/addresses.csv', 'dameformats/files/items.xml', 'dameformats/files/rss.xml', 'dameformats/files/test.nc', 'dameformats/files/example.yaml'])],
      install_requires=[
          'pandas',
          'markdown',
          'pyyaml',
          'netCDF4',
      ],
      test_suite='setup.my_test_suite',
      include_package_data=True,
      zip_safe=False)
