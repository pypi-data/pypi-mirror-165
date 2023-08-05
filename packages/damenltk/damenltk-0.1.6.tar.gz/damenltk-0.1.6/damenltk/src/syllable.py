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

from nltk.corpus import cmudict
import string


class Syllable(object):
    def syllables_in_word(self, word):
        '''Attempts to count the number of syllables in
        the string argument 'word'.
        Limitation: word must be in the CMU dictionary
        (but that was a premise of the Exercise)
        "Algorithm": no. syllables == no. (0,1,2)
        digits in the dictionary entry, right??
        '''
        phoneme_dict = dict(cmudict.entries())
        # although listcomps may be readable,
        # you can't insert print statements to instrument them!!
        if word in phoneme_dict:
            # more destructive; less efficient?
            # NO! see timeit results in my comments below
            return len([ph for ph in phoneme_dict[word]
                        if ph.strip(string.letters)])
        else:
            return 0

    def syllables_in_text(self, text):
        '''Attempts to count the number of syllables
        in the string argument 'text'.
        Limitation: any "internal punctuation" must be part of the word.
        (it wouldn't get "this,and" correctly)
        Lets syllables_in_word do the heavy lifting.
        '''
        # ok, so apparently str.split(delim)
        # only works for A SINGLE CHAR delim...
        # anything fancier, and you might want a regex
        # (and its associated performance penalty)
        # but str.strip(delims) will strip all leading
        # and trailing chars in "delims"!
        # - alternatives at http://stackoverflow.com/questions/265960/
        return sum([syllables_in_word(word.strip(string.punctuation))
                    for word in text.split()])
