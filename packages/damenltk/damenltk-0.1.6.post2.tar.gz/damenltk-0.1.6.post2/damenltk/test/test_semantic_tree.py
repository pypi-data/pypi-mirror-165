#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2021  David Arroyo Menéndez

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
from nltk import CFG
from nltk import bigrams, trigrams
from nltk.corpus import reuters
from collections import Counter, defaultdict


class TddInPythonExample(unittest.TestCase):

    def test_semantic_tree_returns_correct_result(self):
        grammar = CFG.fromstring("""
        S -> NP VP
        PP -> P NP
        NP -> Det N | NP PP
        VP -> V NP | VP PP
        Det -> 'a' | 'the'
        N -> 'dog' | 'cat'
        V -> 'chased' | 'sat'
        P -> 'on' | 'in'
        """)
        self.assertEqual(str(grammar.start()), 'S')
        grammar_str = "[S -> NP VP, "
        grammar_str = grammar_str + "PP -> P NP, "
        grammar_str = grammar_str + "NP -> Det N, "
        grammar_str = grammar_str + "NP -> NP PP, "
        grammar_str = grammar_str + "VP -> V NP, "
        grammar_str = grammar_str + "VP -> VP PP, "
        grammar_str = grammar_str + "Det -> 'a', "
        grammar_str = grammar_str + "Det -> 'the', "
        grammar_str = grammar_str + "N -> 'dog', "
        grammar_str = grammar_str + "N -> 'cat', "
        grammar_str = grammar_str + "V -> 'chased', "
        grammar_str = grammar_str + "V -> 'sat', "
        grammar_str = grammar_str + "P -> 'on', "
        grammar_str = grammar_str + "P -> 'in']"
        self.assertEqual(grammar_str, str(grammar.productions()))

    def test_bigrams_returns_correct_result(self):
        b = list(bigrams(['more', 'is', 'said', 'than', 'done']))
        self.assertEqual([('more', 'is'),
                          ('is', 'said'),
                          ('said', 'than'),
                          ('than', 'done')],
                         list(bigrams(['more', 'is', 'said', 'than', 'done'])))

    def test_first_sentence_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        self.assertEqual(first_sentence[0:3],
                         [u'ASIAN', u'EXPORTERS', u'FEAR'])

    def test_bigrams_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        b = list(bigrams(first_sentence))
        self.assertEqual(b[0:3], [(u'ASIAN', u'EXPORTERS'),
                                  (u'EXPORTERS', u'FEAR'),
                                  (u'FEAR', u'DAMAGE')])

    def test_trigrams_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        t = list(trigrams(first_sentence))
        self.assertEqual(t[0:3],
                         [(u'ASIAN', u'EXPORTERS', u'FEAR'),
                          (u'EXPORTERS', u'FEAR', u'DAMAGE'),
                          (u'FEAR', u'DAMAGE', u'FROM')])

    def test_trigrams_pad_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        t = list(trigrams(first_sentence, pad_left=True, pad_right=True))
        self.assertEqual(t[0:3], [(None, None, u'ASIAN'),
                                  (None, u'ASIAN', u'EXPORTERS'),
                                  (u'ASIAN', u'EXPORTERS', u'FEAR')])
