#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Dameformats.

# Dameformats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Dameformats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Dameformats in the file LICENSE.  If not, see
# <https://www.gnu.org/licenses/>.

from unidecode import unidecode
from xml.dom.minidom import parse, parseString
import re
import os
import csv
import json
import sys


class DameFormats():

    def csvcolumn2list(self, csvpath,  *args, **kwargs):
        # make a list from a column in a csv file
        position = kwargs.get('position', 0)
        header = kwargs.get('header', True)
        delimiter = kwargs.get('delimiter', ',')
        l1 = []
        with open(csvpath) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
            if header:
                next(csvreader, None)
            for row in csvreader:
                l1.append(row[position])
        return l1

    def csv2list(self, csvpath,  *args, **kwargs):
        # make a list from a csv file
        header = kwargs.get('header', False)
        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', "'")
        l1 = []
        with open(csvpath) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            if header:
                next(csvreader, None)
            for row in csvreader:
                l1.append(row)
        return l1

    def num_columns_in_csv(self, csvpath, *args, **kwargs):
        delimiter = kwargs.get('delimiter', ',')
        with open(csvpath, 'r') as csvfile:
            first_line = csvfile.readline()
            ncol = first_line.count(delimiter) + 1
        return ncol

    def is_json(self, myjson):
        # Given a path returns if exist a file that is a json file
        with open(myjson, encoding='utf8') as f:
            text = f.read().strip()
        try:
            json_object = json.loads(text)
        except ValueError as e:
            return False
        f.close()
        return True

    def is_csv(self, mycsv, *args, **kwargs):
        delimiter = kwargs.get('delimiter', ',')
        boolean = False
        if (self.is_json(mycsv)):
            boolean = False
        else:
            with open(mycsv) as f:
                reader = csv.reader(f, delimiter=delimiter)
                try:
                    for row in reader:
                        boolean = True
                except csv.Error as e:
                    return False
        return boolean

    def is_xml(self, myxml):
        try:
            parse(myxml)
            if ("<xml.dom.minidom.Document object" in str(document)):
                bool0 = True
            else:
                bool0 = False
        finally:
            bool0 = False
            return False
        return bool0
