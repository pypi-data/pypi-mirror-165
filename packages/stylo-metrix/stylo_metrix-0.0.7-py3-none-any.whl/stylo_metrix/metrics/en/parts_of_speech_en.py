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


class Part_of_speech(EnglishMetric, ABC):
    category_en = "Parts of speech"
    category_id = 1


class POS_VERB(Part_of_speech):
    name_en = "Incidence of Verbs"
    metric_id = 1

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "v"]
        result = incidence(doc, search)
        return result, {}


class POS_NOUN(Part_of_speech):
    name_en = "Incidence of Nouns"
    metric_id = 2

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "n"]
        result = incidence(doc, search)
        return result, {}


class POS_ADJ(Part_of_speech):
    name_en = "Incidence of Adjectives"
    metric_id = 3

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "adj"]
        result = incidence(doc, search)
        return result, {}


class POS_ADV(Part_of_speech):
    name_en = "Incidence of Adverbs"
    metric_id = 4

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "adv"]
        result = incidence(doc, search)
        return result, {}


class POS_DET(Part_of_speech):
    name_en = "Incidence of Determiners"
    metric_id = 5

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "det"]
        result = incidence(doc, search)
        return result, {}


class POS_INTJ(Part_of_speech):
    name_en = "Incidence of Interjections"
    metric_id = 6

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "intj"]
        result = incidence(doc, search)
        return result, {}


class POS_CONJ(Part_of_speech):
    name_en = "Incidence of Conjunctions"
    metric_id = 7

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "conj"]
        result = incidence(doc, search)
        return result, {}


class POS_PART(Part_of_speech):
    name_en = "Incidence of Particles"
    metric_id = 8

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "part"]
        result = incidence(doc, search)
        return result, {}


class POS_NUM(Part_of_speech):
    name_en = "Incidence of Numerals"
    metric_id = 9

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "num"]
        result = incidence(doc, search)
        return result, {}


class POS_PREP(Part_of_speech):
    name_en = "Incidence of Prepositions"
    metric_id = 10

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "prep"]
        result = incidence(doc, search)
        return result, {}


class POS_PRO(Part_of_speech):
    name_en = "Incidence of Pronouns"
    metric_id = 11

    def count(self, doc):
        search = [token for token in doc._.words if token._.pos == "prep"]
        result = incidence(doc, search)
        return result, {}

PART_OF_SPEECH = [
    POS_VERB,
    POS_NOUN,
    POS_ADJ,
    POS_ADV,
    POS_DET,
    POS_INTJ,
    POS_CONJ,
    POS_PART,
    POS_NUM,
    POS_PREP,
]


parts_of_speech = MetricsGroup([m() for m in PART_OF_SPEECH])
