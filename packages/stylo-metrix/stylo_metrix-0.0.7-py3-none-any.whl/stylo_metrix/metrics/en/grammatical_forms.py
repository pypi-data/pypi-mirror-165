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
from stylo_metrix.structures import Metric, MetricsGroup
from stylo_metrix.utils import incidence


class GrammaticalForms(EnglishMetric, ABC):
    category_en = "Grammatical Forms"
    category_id = 2


class G_WOULD(GrammaticalForms):
    name_en = "Would Simple Incidence"
    metric_id =1

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "would_ind_activ"]
        result = incidence(doc, search)
        return result, {"G_WLD": search}


class G_WOULD_PASSIVE(GrammaticalForms):
    name_en = "Would Passive Incidence"
    metric_id = 2

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "would_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_WLD_P": search}


class G_WOULD_PROGRESSIVE(GrammaticalForms):
    name_en = "Would Continuous Incidence"
    metric_id = 3

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "would_cont"]
        result = incidence(doc, search)
        return result, {"G_WLD_CON": search}


class G_WOULD_PERFECT(GrammaticalForms):
    name_en = "Would Perfect Incidence"
    metric_id = 4

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "would_perf_active"]
        result = incidence(doc, search)
        return result, {"G_WLD_PRF": search}


class G_WOULD_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "Would Perfect Passive Incidence"
    metric_id = 5

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "would_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_WLD_P_P": search}


class G_SHOULD(GrammaticalForms):
    name_en = "Should Simple Incidence"
    metric_id = 6

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "should_ind_active"]
        result = incidence(doc, search)
        return result, {"G_SHLD": search}


class G_SHOULD_PASSIVE(GrammaticalForms):
    name_en = "Should Simple Passive Incidence"
    metric_id = 7

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "should_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_SHLD_P": search}


class G_SHALL(GrammaticalForms):
    name_en = "Shall Simple Incidence"
    metric_id = 8

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "shall_ind_active"]
        result = incidence(doc, search)
        return result, {"G_SHLL": search}


class G_SHALL_PASSIVE(GrammaticalForms):
    name_en = "Shall Simple Passive Incidence"
    metric_id = 9

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "shall_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_SHLL_P": search}


class G_SHOULD_PROGRESSIVE(GrammaticalForms):
    name_en = "Should Continuous Incidence"
    metric_id = 10

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "should_cont"]
        result = incidence(doc, search)
        return result, {"G_SHLD_CON": search}


class G_SHOULD_PERFECT(GrammaticalForms):
    name_en = "Should Perfect Incidence"
    metric_id = 11

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "should_perf_active"]
        result = incidence(doc, search)
        return result, {"G_SHLD_PRF": search}


class G_SHOULD_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "Should Perfect Passive Incidence"
    metric_id = 12

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "should_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_SHLD_P_P": search}


class G_MUST(GrammaticalForms):
    name_en = "Must Simple Incidence"
    metric_id = 13

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "must_ind_active"]
        result = incidence(doc, search)
        return result, {"G_MST": search}


class G_MUST_PASSIVE(GrammaticalForms):
    name_en = "Must Simple Passive Incidence"
    metric_id = 14

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "must_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_MST_P": search}


class G_MUST_PROGRESSIVE(GrammaticalForms):
    name_en = "Must Continuous Incidence"
    metric_id = 15

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "must_cont"]
        result = incidence(doc, search)
        return result, {"G_MST_CON": search}


class G_MUST_PERFECT(GrammaticalForms):
    name_en = "Must Perfect Incidence"
    metric_id = 16

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "must_perf_active"]
        result = incidence(doc, search)
        return result, {"G_MST_PRF": search}


class G_MST_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "Must Perfect Passive Incidence"
    metric_id = 17

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "must_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_MST_P_P": search}


class G_CAN(GrammaticalForms):
    name_en = "Can Simple Incidence"
    metric_id = 18

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "can_ind"]
        result = incidence(doc, search)
        return result, {"G_CAN": search}


class G_CAN_PASSIVE(GrammaticalForms):
    name_en = "Can Simple Passive Incidence"
    metric_id = 19

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "can_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_CAN_P": search}


class G_COULD(GrammaticalForms):
    name_en = "Could Simple Incidence"
    metric_id = 20

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "could_ind"]
        result = incidence(doc, search)
        return result, {"G_CLD": search}


class G_COULD_PASSIVE(GrammaticalForms):
    name_en = "Could Simple Passive Incidence"
    metric_id = 21

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "could_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_CLD_P": search}


class G_CAN_PROGRESSIVE(GrammaticalForms):
    name_en = "Can Continuous Incidence"
    metric_id = 22

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "can_cont"]
        result = incidence(doc, search)
        return result, {"G_CAN_CON": search}


class G_COULD_PROGRESSIVE(GrammaticalForms):
    name_en = "Could Continuous Incidence"
    metric_id = 23

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "could_cont"]
        result = incidence(doc, search)
        return result, {"G_CLD_CON": search}


class G_COULD_PERFECT(GrammaticalForms):
    name_en = "Could Perfect Incidence"
    metric_id = 24

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "could_perf"]
        result = incidence(doc, search)
        return result, {"G_CLD_PRF": search}


class G_COULD_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "Could Perfect Passive Incidence"
    metric_id = 25

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "could_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_CLD_P_P": search}


class G_MAY(GrammaticalForms):
    name_en = "May Simple Incidence"
    metric_id = 26

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "may_ind"]
        result = incidence(doc, search)
        return result, {"G_MAY": search}


class G_MAY_PASSIVE(GrammaticalForms):
    name_en = "May Simple Passive Incidence"
    metric_id = 27

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "may_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_MAY_P": search}


class G_MIGHT(GrammaticalForms):
    name_en = "Might Simple Incidence"
    metric_id = 28

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "might_ind"]
        result = incidence(doc, search)
        return result, {"G_MGHT": search}


class G_MIGHT_PASSIVE(GrammaticalForms):
    name_en = "Might Simple Passive Incidence"
    metric_id = 29

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "might_ind_passive"]
        result = incidence(doc, search)
        return result, {"G_MGHT_P": search}


class G_MAY_PROGRESSIVE(GrammaticalForms):
    name_en = "May Continuous Incidence"
    metric_id = 30

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "may_cont"]
        result = incidence(doc, search)
        return result, {"G_MAY_CON": search}


class G_MIGTH_PERFECT(GrammaticalForms):
    name_en = "Might Perfect Incidence"
    metric_id = 31

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "might_perf"]
        result = incidence(doc, search)
        return result, {"G_MGTH_PRF": search}


#
class G_MIGHT_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "Might Perfect Passive Incidence"
    metric_id = 32

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "might_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_MGHT_PRF_P": search}


class G_MAY_PERFECT_PASSIVE(GrammaticalForms):
    name_en = "May Perfect Passive Incidence"
    metric_id = 33

    def count(self, doc):
        search = [token for token in doc if token._.modal_verbs == "may_perf_passive"]
        result = incidence(doc, search)
        return result, {"G_MAY_PRF_P": search}


class G_ADJ_POSITIVE(GrammaticalForms):
    name_en = "Adjectives Positive Degree Incidence"
    metric_id = 34

    def count(self, doc):
        search = [token for token in doc if token._.adjectives == "positive_adjective"]
        result = incidence(doc, search)
        return result, {"G_ADJ_POS": search}


class G_ADJ_COMPARATIVE(GrammaticalForms):
    name_en = "Adjectives Comparative Degree Incidence"
    metric_id = 35

    def count(self, doc):
        search = [token for token in doc if token._.adjectives == "comparative_adjective"]
        result = incidence(doc, search)
        return result, {"G_ADJ_COMP": search}


class G_ADJ_SUPERLATIVE(GrammaticalForms):
    name_en = "Adjectives Superlative Degree Incidence"
    metric_id = 36

    def count(self, doc):
        search = [token for token in doc if token._.adjectives == "superlative_adjective"]
        result = incidence(doc, search)
        return result, {"G_ADJ_SUP": search}


class G_ADV_POSITIVE(GrammaticalForms):
    name_en = "Adverbs Positive Degree Incidence"
    metric_id = 37

    def count(self, doc):
        search = [token for token in doc if token._.adverbs == "positive_adverb"]
        result = incidence(doc, search)
        return result, {"G_ADV_POS": search}


class G_ADV_COMPARATIVE(GrammaticalForms):
    name_en = "Adverbs Comparative Degree Incidence"
    metric_id = 38

    def count(self, doc):
        search = [token for token in doc if token._.adverbs == "comparative_adverb"]
        result = incidence(doc, search)
        return result, {"G_ADV_COMP": search}


class G_ADV_SUPERLATIVE(GrammaticalForms):
    name_en = "Adverbs Superlative Degree Incidence"
    metric_id = 39

    def count(self, doc):
        search = [token for token in doc if token._.adverbs == "superlative_adverb"]
        result = incidence(doc, search)
        return result, {"G_ADV_SUP": search}


GRAMMATICAL_FORMS = [
    G_WOULD,
    G_WOULD_PASSIVE,
    G_WOULD_PROGRESSIVE,
    G_WOULD_PERFECT,
    G_WOULD_PERFECT_PASSIVE,
    G_SHOULD,
    G_SHOULD_PASSIVE,
    G_SHALL,
    G_SHALL_PASSIVE,
    G_SHOULD_PROGRESSIVE,
    G_SHOULD_PERFECT,
    G_SHOULD_PERFECT_PASSIVE,
    G_MUST,
    G_MUST_PASSIVE,
    G_MUST_PROGRESSIVE,
    G_MUST_PERFECT,
    G_MST_PERFECT_PASSIVE,
    G_CAN,
    G_CAN_PASSIVE,
    G_COULD,
    G_COULD_PASSIVE,
    G_CAN_PROGRESSIVE,
    G_COULD_PROGRESSIVE,
    G_COULD_PERFECT,
    G_COULD_PERFECT_PASSIVE,
    G_MAY,
    G_MAY_PASSIVE,
    G_MIGHT,
    G_MIGHT_PASSIVE,
    G_MAY_PROGRESSIVE,
    G_MIGTH_PERFECT,
    G_MIGHT_PERFECT_PASSIVE,
    G_MAY_PERFECT_PASSIVE,
    G_ADJ_POSITIVE,
    G_ADJ_COMPARATIVE,
    G_ADJ_SUPERLATIVE,
    G_ADV_POSITIVE,
    G_ADV_COMPARATIVE,
    G_ADV_SUPERLATIVE,
]

grammatical_forms_group = MetricsGroup([m() for m in GRAMMATICAL_FORMS])
