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
# along with dameformats; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import json
import pandas as pd
from src.dame_formats import DameFormats
# fix for MacOS using nose
import collections
collections.Callable = collections.abc.Callable


class TestDameJson(unittest.TestCase):

    def test_damejson_load(self):
        # using read and loads to open
        fh = open('files/exer1-interface-data.json')
        jsondata = fh.read()
        json_object = json.loads(jsondata)
        fh.close()
        self.assertEqual(int(json_object['totalCount']), 400)

    def test_damejson_dumps(self):
        self.assertEqual('["foo", {"bar": ["baz", 1.0, 2]}]',
                         json.dumps(['foo', {'bar': ('baz', 1.0, 2)}]))
        self.assertEqual(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True),
                         '{"a": 0, "b": 0, "c": 0}')
        tup1 = 'Red', 'Black', 'White'
        self.assertEqual(json.dumps(tup1), '["Red", "Black", "White"]')

    def test_is_json(self):
        df = DameFormats()
        file1 = "files/exer1-interface-data.json"
        self.assertTrue(df.is_json(file1))
        file2 = "files/min.csv"
        self.assertFalse(df.is_json(file2))

    def test_damejson_pandas(self):
        df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                          index=['row 1', 'row 2'],
                          columns=['col 1', 'col 2'])
        split = df.to_json(orient='split')
        string1 = '{"columns":["col 1","col 2"],'
        string1 = string1 + '"index":["row 1","row 2"],'
        string1 = string1 + '"data":[["a","b"],["c","d"]]}'
        self.assertEqual(string1, split)
        l1 = df.to_json(orient='values')
        self.assertEqual('[["a","b"],["c","d"]]', l1)
        rec = df.to_json(orient='records')
        string1 = '[{"col 1":"a","col 2":"b"},'
        string1 = string1 + '{"col 1":"c","col 2":"d"}]'
        self.assertEqual(string1, rec)
        val = df.to_json(orient='values')
        self.assertEqual('[["a","b"],["c","d"]]', val)


if __name__ == '__main__':
    unittest.main()
