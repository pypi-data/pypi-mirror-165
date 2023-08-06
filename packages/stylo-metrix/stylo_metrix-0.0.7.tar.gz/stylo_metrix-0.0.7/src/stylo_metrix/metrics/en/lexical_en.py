# Copyright (C) 2022  NASK PIB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from abc import ABC

from stylo_metrix.metrics.en.en import EnglishMetric
from stylo_metrix.structures import MetricsGroup
from stylo_metrix.utils import incidence


class Lexical(EnglishMetric, ABC):
    category_en = "Lexical"
    category_id = 4


class L_TYPE_TOKEN_RATIO_LEMMAS(Lexical):
    name_en = "Type-token ratio for words lemmas"
    metric_id = 1

    def count(self, doc):
        types = set(token.lemma_ for token in doc._.words)
        result = incidence(doc, types)
        return result, {}


class L_PROPER_NAME(Lexical):
    name_en = "Incidence of proper names"
    metric_id = 2

    def count(self, doc):
        ents = [token for token in doc if token.pos_ == "PROPN"]
        result = incidence(doc, ents)
        return result, {}


class L_PERSONAL_NAME(Lexical):
    name_en = "Incidence of personal names"
    metric_id = 3

    def count(self, doc):
        ents = [list(ent) for ent in doc.ents if ent.label_ == 'PERSON']
        sum_ents = sum(ents, [])
        result = incidence(doc, sum_ents)
        return result, {}


class L_PUNCT(Lexical):
    name_en = "Incidence of punctuation"
    metric_id = 4

    def count(self, doc):
        ents = [token for token in doc if token.pos_ == "PUNCT"]
        result = incidence(doc, ents)
        return result, {}


class L_PUNCT_DOT(Lexical):
    name_en = "Incidence of dots"
    metric_id = 5

    def count(self, doc):
        ents = [token for token in doc if token.text == "."]
        result = incidence(doc, ents)
        return result, {}


class L_PUNCT_COM(Lexical):
    name_en = "Incidence of comma"
    metric_id = 6

    def count(self, doc):
        ents = [token for token in doc if token.text == ","]
        result = incidence(doc, ents)
        return result, {}


class L_CONT_A(Lexical):
    name_en = "Incidence of Content words"
    metric_id = 7

    def count(self, doc):
        search = [token.text for token in doc._.words if token._.is_content_word]
        result = incidence(doc, search)
        return result, {"CW": search}


class L_FUNC_A(Lexical):
    name_en = "Incidence of Function words"
    metric_id = 8

    def count(self, doc):
        search = [token.text for token in doc._.words if token._.is_function_word]
        result = incidence(doc, search)
        return result, {"CW": search}


class L_CONT_T(Lexical):
    name_en = "Incidence of Content words types"
    metric_id = 9

    def count(self, doc):
        search = set(token.text for token in doc._.words if token._.is_content_word)
        result = incidence(doc, search)
        return result, {}


class L_FUNC_T(Lexical):
    name_en = "Incidence of Function words types"
    metric_id = 10

    def count(self, doc):
        search = set(token.text for token in doc._.words if token._.is_function_word)
        result = incidence(doc, search)
        return result, {}


class L_SYL_G2(Lexical):
    name_en = "Incidence of Words formed of more than 2 syllables"
    metric_id = 11

    def count(self, doc):
        lengths = [token._.syllables_count for token in doc if token._.syllables_count is not None]
        selected = [length for length in lengths if length > 2]
        result = incidence(doc, selected)
        return result, {}


class L_PUNCT_SEMC(Lexical):
    name_en = "Incidence of semicolon"
    metric_id = 12

    def count(self, doc):
        ents = [token for token in doc if token.text == ";"]
        result = incidence(doc, ents)
        return result, {}


class L_PUNCT_COL(Lexical):
    name_en = "Incidence of colon"
    metric_id = 13

    def count(self, doc):
        ents = [token for token in doc if token.text == ":"]
        result = incidence(doc, ents)
        return result, {}


class L_PUNCT_DASH(Lexical):
    name_en = "Incidence of dashes"
    metric_id = 14

    def count(self, doc):
        ents = [token for token in doc if token.text == "—"]
        result = incidence(doc, ents)
        return result, {}


"""
SUBJECT PRONOUNS
"""

class L_I_PRON(Lexical):
    name_en = "Incidence of 'I'-pronoun"
    metric_id = 15

    def count(self, doc):
        pers_pron = [token for token in doc if token.pos_ == "PRON" and ("Person=1" in token.morph) and ("Number=Sing" in token.morph)]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HE_PRON(Lexical):
    name_en = "Incidence of 'he'-pronoun"
    metric_id = 16

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "he"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_SHE_PRON(Lexical):
    name_en = "Incidence of 'she'-pronoun"
    metric_id = 17

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "she"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_IT_PRON(Lexical):
    name_en = "Incidence of 'it'-pronoun"
    metric_id = 18

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "it" and "Case=Nom" in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_YOU_PRON(Lexical):
    name_en = "Incidence of 'you'-pronoun"
    metric_id = 19

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "you" and "Case=Nom" in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_WE_PRON(Lexical):
    name_en = "Incidence of 'we'-pronoun"
    metric_id = 20

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "we"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_THEY_PRON(Lexical):
    name_en = "Incidence of 'they'-pronoun"
    metric_id = 21

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "they"]
        result = incidence(doc, pers_pron)
        return result, {}


"""
OBJECT PRONOUNS
"""

class L_ME_PRON(Lexical):
    name_en = "Incidence of 'me'-pronoun"
    metric_id = 22

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "me"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_YOU_OBJ_PRON(Lexical):
    name_en = "Incidence of 'you'-object pronoun"
    metric_id = 23

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "you" and "Case=Nom" not in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HIM_PRON(Lexical):
    name_en = "Incidence of 'him'-object pronoun"
    metric_id = 24

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "him"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HER_OBJECT_PRON(Lexical):
    name_en = "Incidence of 'her'-object pronoun"
    metric_id = 25

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "her" and "Case=Acc" in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_IT_OBJECT_PRON(Lexical):
    name_en = "Incidence of 'it'-pronoun"
    metric_id = 26

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "it" and "Case=Acc" in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_US_PRON(Lexical):
    name_en = "Incidence of 'us'-pronoun"
    metric_id = 27

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "us"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_THEM_PRON(Lexical):
    name_en = "Incidence of 'them'-pronoun"
    metric_id = 28

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "them"]
        result = incidence(doc, pers_pron)
        return result, {}


"""
POSSESSIVE PRONOUNS
"""

class L_MY_PRON(Lexical):
    name_en = "Incidence of 'my'-pronoun"
    metric_id = 29

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "my"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_YOUR_PRON(Lexical):
    name_en = "Incidence of 'your'-pronoun"
    metric_id = 30

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "your"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HIS_PRON(Lexical):
    name_en = "Incidence of 'his'-pronoun"
    metric_id = 31

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "his"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HER_PRON(Lexical):
    name_en = "Incidence of 'her'-possessive pronoun"
    metric_id = 32

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "her" and "Poss=Yes" in token.morph]
        result = incidence(doc, pers_pron)
        return result, {}


class L_ITS_PRON(Lexical):
    name_en = "Incidence of 'its'-possessive pronoun"
    metric_id = 33

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "its"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_OUR_PRON(Lexical):
    name_en = "Incidence of 'our'-possessive pronoun"
    metric_id = 34

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "our"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_THEIR_PRON(Lexical):
    name_en = "Incidence of 'their'-possessive pronoun"
    metric_id = 35

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "their"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_YOURS_PRON(Lexical):
    name_en = "Incidence of 'yours'-pronoun"
    metric_id = 36

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "yours"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_THEIRS_PRON(Lexical):
    name_en = "Incidence of 'theirs'-pronoun"
    metric_id = 37

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "theirs"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HERS_PRON(Lexical):
    name_en = "Incidence of 'hers'-pronoun"
    metric_id = 38

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "hers"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_OURS_PRON(Lexical):
    name_en = "Incidence of 'ours'-possessive pronoun"
    metric_id = 39

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "ours"]
        result = incidence(doc, pers_pron)
        return result, {}


"""
REFLEXIVE PRONOUNS
"""

class L_MYSELF_PRON(Lexical):
    name_en = "Incidence of 'myself'-pronoun"
    metric_id = 40

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "myself"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_YOURSELF_PRON(Lexical):
    name_en = "Incidence of 'yourself'-pronoun"
    metric_id = 41

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "yourself"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HIMSELF_PRON(Lexical):
    name_en = "Incidence of 'himself'-pronoun"
    metric_id = 42

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "himself"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_HERSELF_PRON(Lexical):
    name_en = "Incidence of 'herself'-pronoun"
    metric_id = 43

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "herself"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_ITSELF_PRON(Lexical):
    name_en = "Incidence of 'itself'-pronoun"
    metric_id = 44

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "itself"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_OURSELVES_PRON(Lexical):
    name_en = "Incidence of 'ourselves'-pronoun"
    metric_id = 45

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "ourselves"]
        result = incidence(doc, pers_pron)
        return result, {}

class L_YOURSELVES_PRON(Lexical):
    name_en = "Incidence of 'yourselves'-pronoun"
    metric_id = 46

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "yourselves"]
        result = incidence(doc, pers_pron)
        return result, {}


class L_THEMSELVES_PRON(Lexical):
    name_en = "Incidence of 'themselves'-pronoun"
    metric_id = 47

    def count(self, doc):
        pers_pron = [token for token in doc if token.lower_ == "themselves"]
        result = incidence(doc, pers_pron)
        return result, {}


"""
POSSESSIVE NOUNS WITH 'S
"""

class L_POSSESSIVES(Lexical):
    name_en = "Incidence of nouns in possessive case"
    metric_id = 48

    def count(self, doc):
        pers_pron = [token for token in doc if token.pos_ == "PART" and token.dep_ == "case"]
        result = incidence(doc, pers_pron)
        return result, {}


LEXICAL = [
    L_TYPE_TOKEN_RATIO_LEMMAS,
    L_PROPER_NAME,
    L_PERSONAL_NAME,
    L_PUNCT,
    L_PUNCT_COM,
    L_PUNCT_SEMC,
    L_PUNCT_COL,
    L_PUNCT_DASH,
    L_CONT_A,
    L_FUNC_A,
    L_CONT_T,
    L_FUNC_T,
    L_SYL_G2,
    L_I_PRON,
    L_HE_PRON,
    L_SHE_PRON,
    L_IT_PRON,
    L_YOU_PRON,
    L_WE_PRON,
    L_THEY_PRON,
    L_ME_PRON,
    L_YOU_OBJ_PRON,
    L_HIM_PRON,
    L_HER_OBJECT_PRON,
    L_IT_OBJECT_PRON,
    L_US_PRON,
    L_THEM_PRON,
    L_MY_PRON,
    L_YOUR_PRON,
    L_HIS_PRON,
    L_HER_PRON,
    L_ITS_PRON,
    L_OUR_PRON,
    L_THEIR_PRON,
    L_YOURS_PRON,
    L_THEIRS_PRON,
    L_HERS_PRON,
    L_OURS_PRON,
    L_MYSELF_PRON,
    L_YOURSELF_PRON,
    L_HIMSELF_PRON,
    L_HERSELF_PRON,
    L_ITSELF_PRON,
    L_OURSELVES_PRON,
    L_YOURSELVES_PRON,
    L_THEMSELVES_PRON,
    L_POSSESSIVES,
]

lexical_group = MetricsGroup([m() for m in LEXICAL])
