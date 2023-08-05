#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez

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

import sys
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import brown, stopwords
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict
from nltk.corpus import names
import string


class DameNLTK(object):
    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)

    def detect_language(self, text):
        """
        Calculate probability of given text to be
        written in several languages and return the
        highest scored.

        It uses a stopwords based approach, counting
        how many unique stopwords are seen in analyzed text.

        @param text: Text whose language want to be detected
        @type text: str
        @return: Most scored language guessed
        @rtype: str
        """
        ratios = self.calculate_languages_ratios(text)
        most_rated_language = max(ratios, key=ratios.get)
        return most_rated_language

    def remove_stopwords_from_string(self, string):
        if not string:
            string = "All work and no play makes jack dull"
            string = string + " boy. All work and no play "
            string = string + "makes jack a dull boy."
        stopWords = set(stopwords.words('english'))
        words = word_tokenize(string)
        wordsFiltered = []

        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)

        return wordsFiltered

    def remove_stopwords_from_array(self, array):
        if not array:
            array = ["All", "work", "and", "no", "play",
                     "makes", "jack", "dull", "boy.",
                     "All", "work", "and", "no", "play",
                     "makes", "jack", "a", "dull", "boy", "."]
        stopWords = set(stopwords.words('english'))
        wordsFiltered = []
        for w in array:
            if w not in stopWords:
                wordsFiltered.append(w)
        return wordsFiltered

    def remove_words_not_in_lang_from_string(self, sent, language):
        words = set(nltk.corpus.words.words(language))
        l1 = []
        for w in nltk.wordpunct_tokenize(sent):
            if w.lower() in words:
                l1.append(w)
        return l1

    def remove_words_not_in_lang_from_array(self, sent, language):
        words = set(nltk.corpus.words.words(language))
        l1 = []
        for w in sent:
            if w.lower() in words:
                l1.append(w)
        return l1

    def calculate_languages_ratios(self, text):
        """
        Calculate probability of given text to be written
        in several languages and return a dictionary
        that looks like
        {'french': 2, 'spanish': 4, 'english': 0}

        @param text: Text whose language want to be detected
        @type text: str

        @return: Dictionary with languages and unique
        stopwords seen in analyzed text
        @rtype: dict
        """
        languages_ratios = {}
        '''
        nltk.wordpunct_tokenize() splits all punctuations
        into separate tokens
        '''
        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]

        # Compute per language included in nltk number of
        # unique stopwords appearing in analyzed text
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)
            num = len(common_elements)  # language "score"
            languages_ratios[language] = num

        return languages_ratios

    def syllables_in_word(self, word):
        '''
        Attempts to count the number of syllables in the
        string argument 'word'
        Limitation: word must be in the CMU dictionary
        (but that was a premise of the Exercise)
        "Algorithm": no. syllables == no. (0,1,2)
        digits in the dictionary entry, right??
        '''
        phoneme_dict = dict(cmudict.entries())
        if word in phoneme_dict:
            return len([ph for ph in phoneme_dict[word]
                        if ph.strip(string.letters)])
        else:
            return 0

    def syllables_in_text(self, text):
        '''
        Attempts to count the number of syllables in
        the string argument 'text'.
        Limitation: any "internal punctuation" must be
        part of the word. (it wouldn't get "this,and"
        correctly)
        Lets syllables_in_word do the heavy lifting.
        '''
        # ok, so apparently str.split(delim) only
        # works for A SINGLE CHAR delim...
        # anything fancier, and you might want a regex
        # (and its associated performance penalty)
        # but str.strip(delims) will strip
        # all leading and trailing chars in "delims"!
        # - alternatives at http://stackoverflow.com/questions/265960/
        return sum([syllables_in_word(word.strip(string.punctuation))
                    for word in text.split()])

    def gender_name(self, name):
        gender = 'undefined'
        if name in names.words('male.txt'):
            gender = 'male'
        if name in names.words('female.txt'):
            if (gender == 'male'):
                gender = 'both'
            else:
                gender = 'female'
        return gender

    def gender_features(self, word):
        return {'last_letter': word[-1]}

    def gender_classifier(self):
        labeled_names = ([(name, 'male')
                          for name in names.words('male.txt')] +
                         [(name, 'female')
                          for name in names.words('female.txt')])
        featuresets = [(self.gender_features(n), gender)
                       for (n, gender) in labeled_names]
        train_set, test_set = featuresets[500:], featuresets[:500]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier
