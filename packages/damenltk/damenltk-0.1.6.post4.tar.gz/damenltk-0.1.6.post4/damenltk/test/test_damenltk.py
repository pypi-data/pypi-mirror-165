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
from nltk.corpus import stopwords
from src.damenltk import DameNLTK


class TddInPythonExample(unittest.TestCase):

    def test_detectlanguage_spanish_method_returns_correct_result(self):
        dn = DameNLTK()
        textes = '''
        En un lugar de la Mancha, de cuyo nombre no quiero acordarme,
        no ha mucho tiempo que vivía un hidalgo de los de lanza en
        astillero, adarga antigua, rocín flaco y galgo corredor.
        Una olla de algo más vaca que carnero, salpicón las más
        noches, duelos y quebrantos los sábados, lantejas los
        viernes, algún palomino de añadidura los domingos, consumían
        las tres partes de su hacienda. El resto della concluían sayo
        de velarte, calzas de velludo para las fiestas, con sus
        pantuflos de lo mesmo, y los días de entresemana se honraba
        con su vellorí de lo más fino. Tenía en su casa una ama que
        pasaba de los cuarenta, y una sobrina que no llegaba a los
        veinte, y un mozo de campo y plaza, que así ensillaba el
        rocín como tomaba la podadera. Frisaba la edad de nuestro
        hidalgo con los cincuenta años; era de complexión recia,
        seco de carnes, enjuto de rostro, gran madrugador y amigo de
        la caza. Quieren decir que tenía el sobrenombre de Quijada, o
        Quesada, que en esto hay alguna diferencia en los autores que
        deste caso escriben; aunque, por conjeturas verosímiles, se
        deja entender que se llamaba Quejana. Pero esto importa poco
        a nuestro cuento; basta que en la narración dél no se salga un
        punto de la verdad.
        En un lugar de la Mancha de cuyo nombre no quiero
        acordarme, vivía un ingenioso hidalgo
        '''
        self.assertEqual(dn.detect_language(textes), "spanish")

    def test_stopwords_remove_method_returns_correct_result(self):
        dn = DameNLTK()
        str1 = '''
        For sequences, (strings, lists, tuples),
        use the fact that empty sequences are false.
        '''
        self.assertEqual(['For', 'sequences', ',', '(', 'strings',
                          ',', 'lists', ',', 'tuples', ')', ',', 'use',
                          'fact', 'empty', 'sequences', 'false', '.'],
                         dn.remove_stopwords_from_string(str1))
        self.assertEqual(['For', 'sequences', ',', '(', 'strings', ',',
                          'lists', ',', 'tuples', ')', ',', 'use', 'fact',
                          'empty', 'sequences', 'false', '.'],
                         dn.remove_stopwords_from_array(
                             ["For", "sequences", ",", "(", "strings", ",",
                              "lists", ",", "tuples", ")", ",", "use", "the",
                              "fact", "that", "empty", "sequences", "are",
                              "false", "."]))

    def test_remove_words_not_in_lang_from_string(self):
        dn = DameNLTK()
        sent = "Io andiamo to the beach with my amico."
        words = dn.remove_words_not_in_lang_from_string(sent, "en")
        self.assertEqual(words, ["Io", "to", "the", "beach", "with", "my"])

    def test_remove_words_not_in_lang_from_array(self):
        dn = DameNLTK()
        sent = ["Io", "andiamo", "to", "the",
                "beach", "with", "my", "amico", "."]
        words = dn.remove_words_not_in_lang_from_array(sent, "en")
        self.assertEqual(words, ["Io", "to", "the", "beach", "with", "my"])

    def test_stopwords_definition_method_returns_correct_result(self):
        st0 = stopwords.words('english')
        st1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
               'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
               'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
               'itself', 'they', 'them', 'their', 'theirs', 'themselves',
               'what', 'which', 'who', 'whom', 'this', 'that', 'these',
               'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
               'being', 'have', 'has', 'had', 'having', 'do', 'does',
               'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
               'or', 'because', 'as', 'until', 'while', 'of', 'at',
               'by', 'for', 'with', 'about', 'against', 'between', 'into',
               'through', 'during', 'before', 'after', 'above', 'below',
               'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
               'under', 'again', 'further', 'then', 'once', 'here', 'there',
               'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
               'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
               'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
               's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
               'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn',
               'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
               'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren',
               'won', 'wouldn']
        self.assertEqual(st0[0], st1[0])
        self.assertEqual(st0[4], st1[4])

    def test_stopwords_spanish_method_returns_correct_result(self):
        st0 = stopwords.words('spanish')
        st1 = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
               'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al',
               'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este',
               'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin',
               'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien',
               'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les',
               'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e',
               'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro',
               'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho',
               'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar',
               'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te',
               'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras',
               'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos',
               'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra',
               'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros',
               'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos',
               'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis',
               'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis',
               'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais',
               'estarían', 'estaba', 'estabas', 'estábamos', 'estabais',
               'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos',
               'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras',
               'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese',
               'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen',
               'estando', 'estado', 'estada', 'estados', 'estadas', 'estad',
               'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas',
               'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá',
               'habremos', 'habréis', 'habrán', 'habría', 'habrías',
               'habríamos', 'habríais', 'habrían', 'había', 'habías',
               'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo',
               'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras',
               'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses',
               'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido',
               'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos',
               'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean',
               'seré', 'serás', 'será', 'seremos', 'seréis', 'serán',
               'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era',
               'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue',
               'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos',
               'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis',
               'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos',
               'sentidas', 'siente', 'sentid', 'tengo', 'tienes', 'tiene',
               'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos',
               'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá',
               'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías',
               'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías',
               'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo',
               'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras',
               'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses',
               'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido',
               'tenida', 'tenidos', 'tenidas', 'tened']
        self.assertEqual(st0[0], "de")
        self.assertEqual(st0[-1], "tened")
