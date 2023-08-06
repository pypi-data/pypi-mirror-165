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


class Verb_Tenses(EnglishMetric, ABC):
    category_en = "Verbs Tenses"
    category_id = 3


class VT_PRESENT_ACTIVE(Verb_Tenses):
    name_en = "Present Tenses Active"
    metric_id = 1

    def count(self, doc):
        label_list = ["present_simple", "present_ind_3p",
                      "present_cont", "present_perfect",
                      "present_perfect_cont"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PASSIVE(Verb_Tenses):
    name_en = "Present Tenses Passive"
    metric_id = 2

    def count(self, doc):
        label_list = ["present_ind_passive", "present_cont_passive",
                      "present_perfect_passive"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_ACTIVE(Verb_Tenses):
    name_en = "Past Tenses Active"
    metric_id = 3

    def count(self, doc):
        label_list = ["past_simple", "past_ind_be",
                      "past_cont", "past_perf", "past_perf_cont"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_PASSIVE(Verb_Tenses):
    name_en = "Past Tenses Passive"
    metric_id = 4

    def count(self, doc):
        label_list = ["past_ind_passive", "past_cont_passive", "past_perf_passive"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_ACTIVE(Verb_Tenses):
    name_en = "Future Tenses Active"
    metric_id = 5

    def count(self, doc):
        label_list = ["future_simple", "future_progr", "future_perfect", "future_perfect_cont"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PASSIVE(Verb_Tenses):
    name_en = "Future Tenses Passive"
    metric_id = 6

    def count(self, doc):
        label_list = ["future_simple_passive", "future_progr_passive", "future_perf_passive"]
        search = [token for token in doc if token._.verb_tense in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_MODALS_ACTIVE(Verb_Tenses):
    name_en = "Modal Verbs Active"
    metric_id = 7

    def count(self, doc):
        label_list = ["would_ind_active", "would_cont", "would_perf_active",
                      "should_ind_active", "shall_ind_active", "should_cont", "should_perf_active",
                      "must_ind_active", "must_cont", "must_perf_active", "can_ind", "could_ind",
                      "can_cont", "could_cont", "could_perf", "may_ind", "might_ind", "may_cont",
                      "might_perf"]
        search = [token for token in doc if token._.modal_verbs in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_MODALS_PASSIVE(Verb_Tenses):
    name_en = "Modal Verbs Active"
    metric_id = 8

    def count(self, doc):
        label_list = ["would_ind_passive", "would_perf_passive", "should_ind_passive",
                      "shall_ind_passive", "should_perf_passive", "must_ind_passive",
                      "must_perf_passive", "can_ind_passive", "could_ind_passive", "could_perf_passive",
                      "may_ind_passive", "might_ind_passive", "might_perf_passive", "may_perf_passive"]
        search = [token for token in doc if token._.modal_verbs in label_list]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_SIMPLE(Verb_Tenses):
    name_en = "Present Simple Tense Incidence"
    metric_id = 9

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_simple"]
        result = incidence(doc, search)

        return result, {}


class VT_PRESENT_SIMPLE_3DPERSN(Verb_Tenses):
    name_en = "Present Simple 3rd Person Incidence"
    metric_id = 10

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_ind_3p"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PROGRESSIVE(Verb_Tenses):
    name_en = "Present Continuous Tense Incidence"
    metric_id = 11

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_cont"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PERFECT(Verb_Tenses):
    name_en = "Present Perfect Tense Incidence"
    metric_id = 12

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_perfect"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PERFECT_PROGR(Verb_Tenses):
    name_en = "Present Prefect Continuous Tense Incidence"
    metric_id = 13

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_perfect_cont"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_SIMPLE_PASSIVE(Verb_Tenses):
    name_en = "Present Simple Passive Incidence"
    metric_id = 14

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_ind_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PROGR_PASSIVE(Verb_Tenses):
    name_en = "Present Continuous Passive Incidence"
    metric_id = 15

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_cont_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_PRESENT_PERFECT_PASSIVE(Verb_Tenses):
    name_en = "Present Perfect Passive Incidence"
    metric_id = 16

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "present_perfect_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_SIMPLE(Verb_Tenses):
    name_en = "Past Simple Tense Incidence"
    metric_id = 17

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_simple"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_SIMPLE_BE(Verb_Tenses):
    name_en = "Past Simple  Incidence'to be'"
    metric_id = 18

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_ind_be"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_PROGR(Verb_Tenses):
    name_en = "Past Continuous Tense Incidence"
    metric_id = 19

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_cont"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_PERFECT(Verb_Tenses):
    name_en = "Past Perfect Tense Incidence"
    metric_id = 20

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_perf"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_PERFECT_PROGR(Verb_Tenses):
    name_en = "Past Perfect Continuous Tense Incidence"
    metric_id = 21

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_perf_cont"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_SIMPLE_PASSIVE(Verb_Tenses):
    name_en = "Past Simple Passive Incidence"
    metric_id = 22

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_ind_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_POGR_PASSIVE(Verb_Tenses):
    name_en = "Past Continuous Passive Incidence"
    metric_id = 23

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_cont_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_PAST_PERFECT_PASSIVE(Verb_Tenses):
    name_en = "Past Perfect Passive Incidence"
    metric_id = 24

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "past_perf_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_SIMPLE(Verb_Tenses):
    name_en = "Future Simple Tense Incidence"
    metric_id = 25

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_simple"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PROGRESSIVE(Verb_Tenses):
    name_en = "Future Continuous Tense Incidence"
    metric_id = 26

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_progr"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PERFECT(Verb_Tenses):
    name_en = "Future Perfect Tense Incidence"
    metric_id = 27

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_perfect"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PERFECT_PROGR(Verb_Tenses):
    name_en = "Future Perfect Continuous Incidence"
    metric_id = 28

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_perfect_cont"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_SIMPLE_PASSIVE(Verb_Tenses):
    name_en = "Future Simple Passive Incidence"
    metric_id = 29

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_simple_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PROGR_PASSIVE(Verb_Tenses):
    name_en = "Future Continuous Passive Incidence"
    metric_id = 30

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_progr_passive"]
        result = incidence(doc, search)
        return result, {}


class VT_FUTURE_PERFECT_PASSIVE(Verb_Tenses):
    name_en = "Present Perfect Passive Incidence"
    metric_id = 31

    def count(self, doc):
        search = [token for token in doc if token._.verb_tense == "future_perf_passive"]
        result = incidence(doc, search)
        return result, {}


TENSES = [
    VT_PRESENT_ACTIVE,
    VT_PRESENT_PASSIVE,
    VT_PAST_ACTIVE,
    VT_PAST_PASSIVE,
    VT_FUTURE_ACTIVE,
    VT_FUTURE_PASSIVE,
    VT_MODALS_ACTIVE,
    VT_MODALS_PASSIVE,
    VT_PRESENT_SIMPLE,
    VT_PRESENT_SIMPLE_3DPERSN,
    VT_PRESENT_PROGRESSIVE,
    VT_PRESENT_PERFECT,
    VT_PRESENT_PERFECT_PROGR,
    VT_PRESENT_SIMPLE_PASSIVE,
    VT_PRESENT_PROGR_PASSIVE,
    VT_PRESENT_PERFECT_PASSIVE,
    VT_PAST_SIMPLE,
    VT_PAST_SIMPLE_BE,
    VT_PAST_PROGR,
    VT_PAST_PERFECT,
    VT_PAST_PERFECT_PROGR,
    VT_PAST_SIMPLE_PASSIVE,
    VT_PAST_POGR_PASSIVE,
    VT_PAST_PERFECT_PASSIVE,
    VT_FUTURE_SIMPLE,
    VT_FUTURE_PROGRESSIVE,
    VT_FUTURE_PERFECT,
    VT_FUTURE_PERFECT_PROGR,
    VT_FUTURE_SIMPLE_PASSIVE,
    VT_FUTURE_PROGR_PASSIVE,
    VT_FUTURE_PERFECT_PASSIVE,
]

verb_tenses_group = MetricsGroup([m() for m in TENSES])
