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
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import inaugural
from nltk.corpus import gutenberg
from nltk.corpus import reuters
from nltk.corpus import cmudict
from nltk.corpus import twitter_samples
from nltk.corpus import verbnet
from nltk.corpus import wordnet
from collections import Counter
# fix for MacOS using nose
import collections
collections.Callable = collections.abc.Callable


class TddInPythonExample(unittest.TestCase):

    def test_corpus_fileids_method_returns_correct_result(self):
        fileids = inaugural.fileids()
        self.assertEqual(['1789-Washington.txt',
                          '1793-Washington.txt',
                          '1797-Adams.txt'], fileids[0:3])

    def test_corpus_bag_of_words_returns_correct_result(self):
        counts = Counter(reuters.words())
        self.assertEqual([('.', 94687), (',', 72360), ('the', 58251),
                          ('of', 35979), ('to', 34035)],
                         counts.most_common(n=5))

    def test_corpus_sents_method_returns_correct_result(self):
        sents1 = [['[', 'Sense', 'and', 'Sensibility',
                   'by', 'Jane', 'Austen', '1811', ']'],
                  ['CHAPTER', '1']]
        self.assertEqual(gutenberg.sents('austen-sense.txt')[0:2], sents1)

    def test_corpus_cat_method_returns_correct_result(self):
        cat = reuters.categories()[0:2]
        self.assertEqual(cat, ['acq', 'alum'])

    def test_corpus_cmudict_method_returns_correct_result(self):
        transcr = cmudict.dict()
        nltk = 'Natural Language Tool Kit'
        t = [transcr[w][0] for w in nltk.lower().split()]
        self.assertEqual(t, [['N', 'AE1', 'CH', 'ER0', 'AH0', 'L'],
                             ['L', 'AE1', 'NG', 'G', 'W', 'AH0', 'JH'],
                             ['T', 'UW1', 'L'], ['K', 'IH1', 'T']])

    def test_corpus_twitter_method_returns_correct_result(self):
        self.assertEqual(twitter_samples.fileids(),
                         ['negative_tweets.json',
                          'positive_tweets.json',
                          'tweets.20150430-223406.json'])
        self.assertEqual(twitter_samples.strings('negative_tweets.json')[0],
                         'hopeless for tmr :(')
        str1 = '#FollowFriday @France_Inte @PKuchly57 @Milipol_Paris for being'
        str1 = str1 + ' top engaged members in my community this week :)'
        tweet = twitter_samples.strings('positive_tweets.json')[0]
        self.assertEqual(tweet, str1)

    def test_corpus_verbnet_method_returns_correct_result(self):
        l1 = ['approve-77', 'characterize-29.2-1-1', 'obtain-13.5.2']
        self.assertEqual(verbnet.classids('accept'), l1)
        self.assertEqual(verbnet.longid('77'), 'approve-77')
        self.assertEqual(verbnet.lemmas()[0:10],
                         ['December', 'FedEx', 'UPS', 'abandon', 'abase',
                          'abash', 'abate', 'abbreviate', 'abduct', 'abet'])

    def test_syn_returns_correct_result(self):
        syns = wordnet.synsets("program")
        # An example of a synset:
        self.assertEqual(syns[0].name(), "plan.n.01")
        # Just the word:
        self.assertEqual(syns[0].lemmas()[0].name(), "plan")
        # Definition of that first synset:
        str1 = "a series of steps to be carried "
        str1 = str1 + "out or goals to be accomplished"
        self.assertEqual(syns[0].definition(), str1)
        # Examples of the word in use in sentences:
        self.assertEqual(syns[0].examples(),
                         ['they drew up a six-step plan',
                          'they discussed plans for a new bond issue'])

    def test_antonym_returns_correct_result(self):
        antonyms = []
        for syn in wordnet.synsets("good"):
            for l1 in syn.lemmas():
                if l1.antonyms():
                    antonyms.append(l1.antonyms()[0].name())
        self.assertEqual(['evil',
                          'evilness',
                          'bad',
                          'badness',
                          'bad',
                          'evil',
                          'ill'],
                         antonyms)
