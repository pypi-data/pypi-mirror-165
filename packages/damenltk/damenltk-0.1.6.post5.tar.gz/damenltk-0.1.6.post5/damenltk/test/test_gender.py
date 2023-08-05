#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2018  David Arroyo Menéndez

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
# along with damenltk; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import nltk
import random
from nltk.corpus import stopwords
from nltk.corpus import names
from src.damenltk import DameNLTK
# fix for MacOS using nose
import collections
collections.Callable = collections.abc.Callable


class TddInPythonExample(unittest.TestCase):

    def test_gender_name_method_returns_correct_result(self):
        dn = DameNLTK()
        self.assertTrue(dn.gender_name("Neo"), "male")
        self.assertTrue(dn.gender_name("Trinity"), "female")
        self.assertTrue(dn.gender_name("Andrea"), "both")

    def test_gender_classifier_method_returns_correct_result(self):
        dn = DameNLTK()
        classifier = dn.gender_classifier()
        neo = dn.gender_features("Neo")
        self.assertTrue(classifier.classify(neo), "male")
        trinity = dn.gender_features("Trinity")
        self.assertTrue(classifier.classify(trinity), "female")
