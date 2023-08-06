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
# along with damejson; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import json
import pandas as pd
import yaml

# fix for MacOS using nose
import collections
collections.Callable = collections.abc.Callable


class TestDameYaml(unittest.TestCase):

    def test_dameyaml_load(self):
        # using read and loads to open
        yaml_file = open("files/example.yaml", 'r')
        yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
        self.assertEqual(len(yaml_content.items()), 7)

    def test_dameyaml_dumps(self):
        dict_file = [{'sports':
                      ['soccer', 'football',
                       'basketball', 'cricket',
                       'hockey', 'table tennis']},
                     {'countries':
                      ['Pakistan', 'USA',
                       'India', 'China',
                       'Germany', 'France',
                       'Spain']}]
        with open(r'files/dump_file.yaml', 'w') as file:
            documents = yaml.dump(dict_file, file)
        self.assertFalse(documents)


if __name__ == '__main__':
    unittest.main()
