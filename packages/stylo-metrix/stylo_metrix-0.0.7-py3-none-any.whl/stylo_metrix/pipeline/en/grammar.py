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


from stylo_metrix.pipeline.en.dictionary_en import TAGS_DICT, WORDS_POS, FUNCTION_WORDS


def classify_pos(token):
    for custom_pos, pos in TAGS_DICT.items():
        if token.pos_ in pos:
            return custom_pos


def is_word(token):
    return token._.pos in WORDS_POS


def is_function_word(token):
    if token.lemma_ in FUNCTION_WORDS:
        return True


def is_content_word(token):
    if token._.is_word and token.lemma_ and not token._.is_function_word:
        return True


"""GRAMMATICAL TENSES"""

""" METRICS FOR THE PRESENT TENSES [PASSIVE & ACTIVE VOICE]"""


def present_simple(doc):
    present_simple = set()
    label = "present_simple"
    ext = "verb_tense"

    for token in doc:
        if token.tag_ == "VBP" and [child.pos_ != "AUX" for child in token.children]:
            present_simple.add(token)

    for token in doc:
        if token.lemma_ == "do" and (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VB":
            head = token.head
            present_simple.add(head)
            present_simple.add(token)

            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    present_simple.add(t)
    return present_simple, ext, label


def present_ind_3p(doc):
    present_ind_3p = set()
    label = "present_ind_3p"
    ext = "verb_tense"

    for token in doc:
        if token.tag_ == "VBZ" and [child.pos_ != "AUX" for child in token.children]:
            present_ind_3p.add(token)

    return present_ind_3p, ext, label


def present_cont(doc):
    present_cont = set()
    label = "present_cont"
    ext = "verb_tense"

    for token in doc:

        if token.lemma_ == "be" and (
                token.tag_ == "VBZ" or token.tag_ == "VBP") and token.dep_ == "aux" and token.head.tag_ == "VBG":
            head = token.head
            present_cont.add(head)
            present_cont.add(token)

            for t in head.subtree:
                if t.tag_ == "VBG" and t.dep_ == "conj":
                    present_cont.add(t)

    return present_cont, ext, label


def present_perfect_cont(doc):
    present_perfect_cont = set()
    label = "present_perfect_cont"
    ext = "verb_tense"

    for token in doc:
        if token.dep_ == "auxpass" and (token.text == "'s" or token.text == "’s") and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "been" and t.dep_ == "aux":
                    present_perfect_cont.add(head)
                    present_perfect_cont.add(token)
                    present_perfect_cont.add(t)

                for i in head.subtree:
                    if i.tag_ == "VBG" and i.dep_ == "conj":
                        present_perfect_cont.add(i)

        if token.dep_ == "aux" and token.lemma_ == "'ve" and token.head.tag_ == "VBG":
            head = token.head

            for tok in head.subtree:
                if tok.text == "been" and tok.dep_ == "aux":
                    present_perfect_cont.add(head)
                    present_perfect_cont.add(token)
                    present_perfect_cont.add(tok)

            for j in head.subtree:
                if j.tag_ == "VBG" and j.dep_ == "conj":
                    present_perfect_cont.add(j)

        if token.lemma_ == "have" and (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VBG":
            head = token.head

            for tkn in head.subtree:
                if tkn.text == "been" and tkn.dep_ == "aux":
                    present_perfect_cont.add(head)
                    present_perfect_cont.add(token)
                    present_perfect_cont.add(tkn)

            for l in head.subtree:
                if l.tag_ == "VBG" and l.dep_ == "conj":
                    present_perfect_cont.add(l)

    return present_perfect_cont, ext, label


def present_ind_pas(doc):
    present_ind_pas = set()
    label = "present_ind_passive"
    ext = "verb_tense"

    for token in doc:
        if (
                token.tag_ == "VBP" or token.tag_ == "VBZ") and token.dep_ == "auxpass" and token.lemma_ == 'be' and token.head.tag_ == "VBN":
            head = token.head
            present_ind_pas.add(head)

            for child in head.subtree:
                if child.text == "been" and child.dep_ == "auxpass" and head in present_ind_pas:
                    present_ind_pas.remove(head)
                if child.text == "been" and child.dep_ == "ROOT" and head in present_ind_pas:
                    present_ind_pas.remove(head)
            if head in present_ind_pas:
                present_ind_pas.add(token)
            for t in head.children:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in present_ind_pas:
                    present_ind_pas.add(t)
    return present_ind_pas, ext, label


def present_cont_pas(doc):
    present_cont_pas = set()
    label = "present_cont_passive"
    ext = "verb_tense"

    for token in doc:
        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.lemma_ == "be" and token.dep_ == "aux":
            head = token.head

            for t in head.subtree:
                if t.text == "being" and t.dep_ == "auxpass" and head not in present_cont_pas:
                    present_cont_pas.add(head)
                    present_cont_pas.add(t)
                    present_cont_pas.add(token)

                    if t.tag_ == "VBN" and t.dep_ == "conj":
                        present_cont_pas.add(t)
    return present_cont_pas, ext, label


def present_perfect_passive(doc):
    present_perfect_passive = set()
    label = "present_perfect_passive"
    ext = "verb_tense"

    for token in doc:
        if token.lemma_ == "have" and (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VBN":
            head = token.head

            for t in head.subtree:
                if t.text == "been" and t.dep_ == "auxpass" and head not in present_perfect_passive:
                    present_perfect_passive.add(head)
                    present_perfect_passive.add(token)
                    present_perfect_passive.add(t)

            for tok in head.children:
                if tok.tag_ == "VBN" and tok.dep_ == "conj" and head in present_perfect_passive:
                    present_perfect_passive.add(tok)

        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VBN":
            head = token.head

            for j in head.subtree:
                if j.text == "been" and j.dep_ == "auxpass" and head not in present_perfect_passive:
                    present_perfect_passive.add(head)
                    present_perfect_passive.add(token)
                    present_perfect_passive.add(j)

            for tkn in head.children:
                if tkn.tag_ == "VBN" and tkn.dep_ == "conj" and head in present_perfect_passive:
                    present_perfect_passive.add(tkn)

    return present_perfect_passive, ext, label


def present_perfect(doc):
    present_perfect = []
    label = "present_perfect"
    ext = "verb_tense"

    verbs_perfect_passive, _, _ = present_perfect_passive(doc)
    verbs_ind_pas, _, _ = present_ind_pas(doc)
    verbs_cont_pas, _, _ = present_cont_pas(doc)

    for token in doc:

        if token.lemma_ == "have" and (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VBN":
            head = token.head
            present_perfect.append(head)
            present_perfect.append(token)

            for key in verbs_perfect_passive:
                for verb in present_perfect:
                    if key == verb:
                        present_perfect.remove(head)
                        present_perfect.remove(token)

            for tok in head.subtree:
                if head in present_perfect:
                    if tok.tag_ == "VBN" and tok.dep_ == "conj":
                        present_perfect.append(tok)

        if (token.tag_ == "VBZ" or token.tag_ == "VBP") and token.head.tag_ == "VBN":
            head = token.head
            present_perfect.append(head)

            for key in verbs_perfect_passive:
                for verb in present_perfect:
                    if head in present_perfect and key == verb:
                        present_perfect.remove(head)

            for key in verbs_ind_pas:
                for verb in present_perfect:
                    if head in present_perfect and key == verb:
                        present_perfect.remove(head)

            for key in verbs_cont_pas:
                for verb in present_perfect:
                    if head in present_perfect and key == verb:
                        present_perfect.remove(head)

            for tok in head.subtree:
                if head in present_perfect:
                    if tok.tag_ == "VBN" and tok.dep_ == "conj" and head in present_perfect and tok not in present_perfect:
                        present_perfect.append(tok)

    present_perfect_ = set(present_perfect)
    return present_perfect_, ext, label


""" METRICS FOR THE PAST TENSES [PASSIVE & ACTIVE VOICE]"""


def past_simple_passive(doc):
    past_ind_passive = set()
    label = "past_ind_passive"
    ext = "verb_tense"

    for token in doc:

        if token.lemma_ == "be" and token.tag_ == "VBD" and token.dep_ == "auxpass" and token.head.tag_ == "VBN":
            head = token.head
            past_ind_passive.add(head)

            for child in head.children:
                if child.text == "been" and child.dep_ == "auxpass":
                    past_ind_passive.remove(head)

            for tok in head.subtree:
                if tok.tag_ == "VBN" and tok.dep_ == "conj":
                    past_ind_passive.add(tok)

            if head in past_ind_passive:
                past_ind_passive.add(token)

    return past_ind_passive, ext, label


def past_simple(doc):
    past_ind = set()
    label = "past_simple"
    ext = "verb_tense"

    for token in doc:
        if token.lemma_ == "be":
            continue
        if token.lemma_ == "have" and [child.tag_ == "VBN" for child in token.children]:
            continue
        if token.pos_ != "AUX" and token.tag_ == "VBD":
            past_ind.add(token)

        if token.lemma_ == "do" and token.tag_ == "VBD" and token.head.tag_ == "VB":
            head = token.head
            past_ind.add(head)
            past_ind.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    past_ind.add(t)

    return past_ind, ext, label


def past_simple_be(doc):
    past_ind_be = set()
    label = "past_ind_be"
    ext = "verb_tense"

    for token in doc:
        for child in token.children:
            if token.lemma_ == "be" and token.tag_ == "VBD" and child.tag_ != "VBG" and token not in past_ind_be:
                past_ind_be.add(token)

    return past_ind_be, ext, label


def past_cont_passive(doc):
    past_cont_passive = set()
    label = "past_cont_passive"
    ext = "verb_tense"

    for token in doc:
        if token.lemma_ == "be" and token.tag_ == "VBD" and token.head.tag_ == "VBN":
            head = token.head

            for child in head.children:
                if child.text == "being" and child.tag_ == "VBG":
                    past_cont_passive.add(head)
                    past_cont_passive.add(child)
                    past_cont_passive.add(token)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in past_cont_passive and t not in past_cont_passive:
                    past_cont_passive.add(t)

    return past_cont_passive, ext, label


def past_cont(doc):
    past_cont = set()
    label = "past_cont"
    ext = "verb_tense"

    for token in doc:
        if token.lemma_ == "be" and token.tag_ == "VBD" and token.head.tag_ == "VBG":
            head = token.head
            past_cont.add(head)
            past_cont.add(token)
            for t in head.subtree:
                if t.tag_ == "VBG" and t.dep_ == "conj" and t not in past_cont:
                    past_cont.add(t)
    return past_cont, ext, label


def past_perfect(doc):
    past_perf = set()
    label = "past_perf"
    ext = "verb_tense"

    for token in doc:
        if token.tag_ == "VBD" and token.dep_ == "aux" and token.lemma_ == "have" and token.head.tag_ == "VBN":
            head = token.head
            past_perf.add(head)

            for child in head.children:
                if child.text == "been" and child.dep_ == "auxpass":
                    past_perf.remove(head)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in past_perf and t not in past_perf:
                    past_perf.add(t)

        if (token.text == "'d" or token.text == "’d") and (token.head.tag_ == "VBN" or token.head.tag_ == "VBD"):
            head = token.head
            past_perf.add(head)

            for child in head.children:
                if child.lemma_ == "be" and child.dep_ == "auxpass" and head in past_perf:
                    past_perf.remove(head)

            for tok in head.subtree:
                if tok.tag_ == "VBN" and tok.dep_ == "conj" and head in past_perf and tok not in past_perf:
                    past_perf.add(tok)

            if head in past_perf:
                past_perf.add(token)

    return past_perf, ext, label


def past_perf_passive(doc):
    past_perf_passive = set()
    label = "past_perf_passive"
    ext = "verb_tense"

    for token in doc:
        if token.tag_ == "VBD" and token.lemma_ == "have" and token.head.tag_ == "VBN":
            head = token.head

            for child in head.children:
                if child.text == "been" and child.dep_ == "auxpass":
                    past_perf_passive.add(head)
                    past_perf_passive.add(token)
                    past_perf_passive.add(child)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in past_perf_passive and t not in past_perf_passive:
                    past_perf_passive.add(t)

                    # make sure that no past simple passive verbs are regarded as
                    # synonyms of the past perfect passive
                    for ch in t.children:
                        if ch.lemma_ == "be" and (ch.tag_ == "VBD" or ch.tag_ == "VBG") and t in past_perf_passive:
                            past_perf_passive.remove(t)

        if (token.text == "'d" or token.text == "’d") and token.head.tag_ == "VBN":
            head = token.head

            for child in head.children:
                if child.lemma_ == "be" and child.dep_ == "auxpass":
                    past_perf_passive.add(head)
                    past_perf_passive.add(token)
                    past_perf_passive.add(child)

            for tok in head.subtree:
                if tok.tag_ == "VBN" and tok.dep_ == "conj" and head in past_perf_passive:
                    past_perf_passive.add(tok)

                    for chld in tok.children:
                        if chld.lemma_ == "be" and (
                                chld.tag_ == "VBD" or chld.tag_ == "VBG") and tok in past_perf_passive:
                            past_perf_passive.remove(tok)

    return past_perf_passive, ext, label


def past_perfect_cont(doc):
    past_perfect_cont = set()
    label = "past_perf_cont"
    ext = "verb_tense"

    for token in doc:
        if token.tag_ == "VBD" and token.lemma_ == "have" and token.head.tag_ == "VBG":
            head = token.head
            past_perfect_cont.add(head)
            past_perfect_cont.add(token)

            for j in head.children:
                if j.text == "been":
                    past_perfect_cont.add(j)

            for t in head.subtree:
                if t.tag_ == "VBG" and t.dep_ == "conj" and t not in past_perfect_cont:
                    past_perfect_cont.add(t)

    return past_perfect_cont, ext, label


""" METRICS FOR THE FUTURE TENSES [PASSIVE & ACTIVE VOICE]"""


def future_simple(doc):
    future_simple = set()
    label = "future_simple"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VB" and token.head not in future_simple:
            head = token.head

            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ != "xcomp":
                    future_simple.add(t)
                    future_simple.add(token)

    return future_simple, ext, label


def future_simple_passive(doc):
    future_simple_passive = set()
    label = "future_simple_passive"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[
            len(str(token)) - 2:] == "ll" or token.lemma_ == "will") and \
                token.head.tag_ == "VBN" and token.head not in future_simple_passive:
            head = token.head

            for t in head.children:
                if t.text == "be" and t.dep_ == "auxpass":
                    future_simple_passive.add(head)
                    future_simple_passive.add(token)
                    future_simple_passive.add(t)

            for child in head.subtree:
                if child.tag_ == "VBN" and child.dep_ == "conj" and head in future_simple_passive:
                    future_simple_passive.add(child)

                    for ch in child.children:
                        if (ch.text == "being" or ch.text == "been") and ch.dep_ == "auxpass" and child in future_simple_passive:
                            future_simple_passive.remove(child)

    return future_simple_passive, ext, label


def future_cont(doc):
    future_progr = set()
    label = "future_progr"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VBG" and token.head not in future_progr:

            head = token.head
            future_progr.add(head)

            for t in head.subtree:
                if t.lemma_ == "have" and head in future_progr:
                    future_progr.remove(head)

                if t.tag_ == "VBG" and t.dep_ == "conj":
                    future_progr.add(t)

            if head in future_progr:
                future_progr.add(token)

            for j in head.children:
                if j.text == "be":
                    future_progr.add(j)
    return future_progr, ext, label


def future_progr_passive(doc):
    future_progr_passive = set()
    label = "future_progr_passive"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VBN" and token.head not in future_progr_passive:
            head = token.head

            for t in head.children:
                if t.text == "being" and t.dep_ == "auxpass":
                    future_progr_passive.add(head)
                    future_progr_passive.add(t)
                    future_progr_passive.add(token)

                if t.text == "be" and head in future_progr_passive:
                    future_progr_passive.add(t)
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in future_progr_passive:
                    future_progr_passive.add(t)

                    for chld in t.children:
                        if chld.text == "be" or chld.text == "been" and chld.dep_ == "auxpass" and t in future_progr_passive:
                            future_progr_passive.remove(t)
    return future_progr_passive, ext, label


def future_perfect(doc):
    future_perfect = set()
    label = "future_perfect"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VBN" and token.head not in future_perfect:
            head = token.head

            for t in head.children:
                if t.lemma_ == "have" and t.dep_ == "aux":
                    future_perfect.add(head)
                if t.text == "been" and t.dep_ == "auxpass" and head in future_perfect:
                    future_perfect.remove(head)

            for tok in head.subtree:
                if tok.tag_ == "VBN" and tok.dep_ == "conj" and head in future_perfect:
                    future_perfect.add(tok)

                for chld in tok.children:
                    if (chld.text == "being" or chld.text == "be") and tok in future_perfect:
                        future_perfect.remove(tok)

            if head in future_perfect:
                for k in head.children:
                    if k.text == "have":
                        future_perfect.add(k)
                    if k.text == "been":
                        future_perfect.add(k)

    return future_perfect, ext, label


def future_perfect_passive(doc):
    future_perf_passive = set()
    label = "future_perf_passive"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VBN" and token.head not in future_perf_passive:
            head = token.head

            for child in head.children:
                if child.text == "been" and child.dep_ == "auxpass":
                    future_perf_passive.add(head)
                    future_perf_passive.add(token)
                    future_perf_passive.add(child)

            for chld in head.subtree:
                if chld.tag_ == "VBN" and chld.dep_ == "conj" and head in future_perf_passive:
                    future_perf_passive.add(chld)

                for t in chld.children:
                    if (t.text == "be" or t.text == "being") and t.dep_ == "auxpass" and chld in future_perf_passive:
                        future_perf_passive.remove(chld)

    return future_perf_passive, ext, label


def future_perf_cont(doc):
    future_perfect_cont = set()
    label = "future_perfect_cont"
    ext = "verb_tense"

    for token in doc:
        if (str(token)[len(str(token)) - 2:] == "ll" or token.lemma_ == "will") \
                and token.head.tag_ == "VBG" and token.head not in future_perfect_cont:
            head = token.head

            for t in head.children:
                if t.tag_ == "VBN" and t.lemma_ == "be":
                    future_perfect_cont.add(head)
                    future_perfect_cont.add(t)
                    future_perfect_cont.add(token)
    return future_perfect_cont, ext, label


""" METRICS FOR MODAL VERBS [PASSIVE & ACTIVE VOICE]"""


def would_ind_active(doc):
    would_ind_active = set()
    label = "would_ind_active"
    ext = "modal_verbs"

    for token in doc:
        if token.lemma_ == "would" and token.head.tag_ == "VB":
            head = token.head
            would_ind_active.add(head)
            would_ind_active.add(token)

            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    would_ind_active.add(t)
    return would_ind_active, ext, label


def would_ind_passive(doc):
    would_ind_passive = set()
    label = "would_ind_passive"
    ext = "modal_verbs"

    for token in doc:
        if token.lemma_ == "would" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    would_ind_passive.add(head)
                    would_ind_passive.add(token)
                    would_ind_passive.add(tkn)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in would_ind_passive:
                    would_ind_passive.add(t)

    return would_ind_passive, ext, label


def would_cont_active(doc):
    would_cont_active = set()
    ext = "modal_verbs"
    label = "would_cont"

    for token in doc:

        if token.lemma_ == "would" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    would_cont_active.add(head)
                    would_cont_active.add(t)
                    would_cont_active.add(token)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            would_cont_active.add(j)
    return would_cont_active, ext, label


def would_perf_active(doc):
    would_perf_active = set()
    label = "would_perf_active"
    ext = "modal_verbs"

    for token in doc:
        if (token.lemma_ == "would" or token.lemma_ == "'d" or token.lemma_ == "’d") and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.lemma_ == "have":
                    would_perf_active.add(head)

            for k in head.children:
                if k.lemma_ == "be" and head in would_perf_active:
                    would_perf_active.remove(head)

            if head in would_perf_active:
                would_perf_active.add(token)
                for tkn in head.children:
                    if tkn.lemma_ == "have":
                        would_perf_active.add(tkn)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj" and head in would_perf_active:
                    would_perf_active.add(j)

    return would_perf_active, ext, label


def would_perf_passive(doc):
    would_perf_passive = set()
    label = "would_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if (token.lemma_ == "would" or token.lemma_ == "'d" or token.lemma_ == "’d") and token.head.tag_ == "VBN":
            head = token.head

            for k in head.children:
                if k.text == "been" and k.dep_ == "auxpass":
                    would_perf_passive.add(head)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj" and head in would_perf_passive:
                    would_perf_passive.add(j)

    return would_perf_passive, ext, label


def should_ind_active(doc):
    should_ind_active = set()
    label = "should_ind_active"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "should" and token.head.tag_ == "VB":
            head = token.head
            should_ind_active.add(head)
            should_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    should_ind_active.add(t)
    return should_ind_active, ext, label


def should_ind_passive(doc):
    should_ind_passive = set()
    label = "should_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "should" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    should_ind_passive.add(head)
                    should_ind_passive.add(tkn)
                    should_ind_passive.add(token)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in should_ind_passive:
                    should_ind_passive.add(t)
    return should_ind_passive, ext, label


def shall_ind_active(doc):
    shall_ind_active = set()
    label = "shall_ind_active"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "shall" and token.head.tag_ == "VB":
            head = token.head
            shall_ind_active.add(head)
            shall_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    shall_ind_active.add(t)
    return shall_ind_active, ext, label


def shall_ind_passive(doc):
    shall_ind_passive = set()
    label = "shall_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "shall" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    shall_ind_passive.add(head)
                    shall_ind_passive.add(tkn)
                    shall_ind_passive.add(token)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in shall_ind_passive:
                    shall_ind_passive.add(t)
    return shall_ind_passive, ext, label


def should_cont(doc):
    should_cont = set()
    label = "should_cont"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "should" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    should_cont.add(head)
                    should_cont.add(t)
                    should_cont.add(token)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            should_cont.add(j)
    return should_cont, ext, label


def should_perf_active(doc):
    should_perf_active = set()
    label = "should_perf_active"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "should" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.text == "have":
                    should_perf_active.add(head)
                    should_perf_active.add(t)

                    for k in head.children:
                        if k.text == "been" and k.dep_ != "ROOT" and (head in should_perf_active):
                            should_perf_active.remove(head)
                            should_perf_active.remove(t)

            if head in should_perf_active:
                should_perf_active.add(token)

            for k in head.subtree:
                if (k.tag_ == "VBN" or k.tag_ == "VBD") and k.dep_ == "conj" and head in should_perf_active:
                    should_perf_active.add(k)
    return should_perf_active, ext, label


def should_perf_passive(doc):
    should_perf_passive = set()
    label = "should_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "should" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.text == "been" and t.dep_ == "auxpass":
                    should_perf_passive.add(head)
                    should_perf_passive.add(t)
                    should_perf_passive.add(token)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj" and head in should_perf_passive:
                    should_perf_passive.add(j)
    return should_perf_passive, ext, label


def must_ind_active(doc):
    must_ind_active = set()
    label = "must_ind_active"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "must" and token.head.tag_ == "VB":
            head = token.head
            must_ind_active.add(head)
            must_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    must_ind_active.add(t)
    return must_ind_active, ext, label


def must_ind_passive(doc):
    must_ind_passive = set()
    label = "must_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "must" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    must_ind_passive.add(head)
                    must_ind_passive.add(token)
                    must_ind_passive.add(tkn)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in must_ind_passive:
                    must_ind_passive.add(t)
    return must_ind_passive, ext, label


def must_cont(doc):
    must_cont = set()
    label = "must_cont"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "must" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    must_cont.add(head)
                    must_cont.add(token)
                    must_cont.add(t)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            must_cont.add(j)
    return must_cont, ext, label


def must_perf_active(doc):
    must_perf_active = set()
    label = "must_perf_active"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "must" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.subtree:
                if t.text == "have":
                    must_perf_active.add(head)
                    must_perf_active.add(t)

                    for tkn in head.children:
                        if tkn.text == "been" and tkn.dep_ != "ROOT":
                            must_perf_active.remove(head)
                            must_perf_active.remove(t)

            if head in must_perf_active:
                must_perf_active.add(token)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj":
                    must_perf_active.add(j)
    return must_perf_active, ext, label


def must_perf_passive(doc):
    must_perf_passive = set()
    label = "could_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "must" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "been" and tkn.dep_ == "auxpass":
                    must_perf_passive.add(head)
                    must_perf_passive.add(token)
                    must_perf_passive.add(tkn)

                    for tkn in head.children:
                        if tkn.lemma_ == "have":
                            must_perf_passive.add(tkn)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj" and head in must_perf_passive:
                    must_perf_passive.add(j)
    return must_perf_passive, ext, label


def can_ind(doc):
    can_ind = set()
    label = "can_ind"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "can" and token.head.tag_ == "VB":
            head = token.head
            can_ind.add(head)
            can_ind.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    can_ind.add(t)
    return can_ind, ext, label


def can_ind_passive(doc):
    can_present_ind_passive = set()
    label = "can_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "can" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    can_present_ind_passive.add(head)
                    can_present_ind_passive.add(tkn)
                    can_present_ind_passive.add(token)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in can_present_ind_passive:
                    can_present_ind_passive.add(t)

    return can_present_ind_passive, ext, label


def could_ind_active(doc):
    could_ind_active = set()
    label = "could_ind"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "could" and token.head.tag_ == "VB":
            head = token.head
            could_ind_active.add(head)
            could_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    could_ind_active.add(t)
    return could_ind_active, ext, label


def could_ind_passive(doc):
    could_ind_passive = set()
    label = "could_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "could" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    could_ind_passive.add(head)
                    could_ind_passive.add(token)
                    could_ind_passive.add(tkn)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in could_ind_passive:
                    could_ind_passive.add(t)
    return could_ind_passive, ext, label


def can_cont(doc):
    can_cont = set()
    label = "can_cont"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "can" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    can_cont.add(head)
                    can_cont.add(t)
                    can_cont.add(token)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            can_cont.add(j)
    return can_cont, ext, label


def could_cont(doc):
    could_cont = set()
    label = "could_cont"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "could" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    could_cont.add(head)
                    could_cont.add(token)
                    could_cont.add(t)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            could_cont.add(j)
    return could_cont, ext, label


def could_perf_active(doc):
    could_perf_active = set()
    label = "could_perf"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "could" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.subtree:
                if t.lemma_ == "have":
                    could_perf_active.add(head)
                    could_perf_active.add(t)

                    for j in head.subtree:
                        if j.text == "been" and j.dep_ != "ROOT" and (head in could_perf_active):
                            could_perf_active.remove(head)
                            could_perf_active.remove(t)

            if head in could_perf_active:
                could_perf_active.add(token)

            for k in head.subtree:
                if k.tag_ == "VBN" and k.dep_ == "conj" and head in could_perf_active:
                    could_perf_active.add(k)
    return could_perf_active, ext, label


def could_perf_passive(doc):
    could_perf_passive = set()
    label = "could_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "could" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.text == "been":
                    could_perf_passive.add(head)
                    could_perf_passive.add(t)
                    could_perf_passive.add(token)

                    for k in head.children:
                        if k.lemma_ == "have":
                            could_perf_passive.add(k)

            for i in head.subtree:
                if i.tag_ == "VBN" and i.dep_ == "conj" and head in could_perf_passive:
                    could_perf_passive.add(i)
    return could_perf_passive, ext, label


def may_ind_active(doc):
    may_ind_active = set()
    label = "may_ind"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "may" and token.head.tag_ == "VB":
            head = token.head
            may_ind_active.add(head)
            may_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    may_ind_active.add(t)
    return may_ind_active, ext, label


def may_ind_passive(doc):
    may_ind_passive = set()
    label = "may_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "may" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    may_ind_passive.add(head)
                    may_ind_passive.add(tkn)
                    may_ind_passive.add(token)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in may_ind_passive:
                    may_ind_passive.add(t)
    return may_ind_passive, ext, label


def might_ind_active(doc):
    might_ind_active = set()
    label = "might_ind"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "might" and token.head.tag_ == "VB":
            head = token.head
            might_ind_active.add(head)
            might_ind_active.add(token)
            for t in head.subtree:
                if t.tag_ == "VB" and t.dep_ == "conj":
                    might_ind_active.add(t)
    return might_ind_active, ext, label


def might_ind_passive(doc):
    might_ind_passive = set()
    label = "might_ind_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "might" and token.head.tag_ == "VBN":
            head = token.head

            for tkn in head.children:
                if tkn.text == "be" and tkn.dep_ == "auxpass":
                    might_ind_passive.add(head)
                    might_ind_passive.add(token)
                    might_ind_passive.add(tkn)

            for t in head.subtree:
                if t.tag_ == "VBN" and t.dep_ == "conj" and head in might_ind_passive:
                    might_ind_passive.add(t)
    return might_ind_passive, ext, label


def may_cont(doc):
    may_cont = set()
    label = "may_cont"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "may" and token.head.tag_ == "VBG":
            head = token.head

            for t in head.subtree:
                if t.text == "be":
                    may_cont.add(head)
                    may_cont.add(token)
                    may_cont.add(t)

                    for j in head.subtree:
                        if j.tag_ == "VBG" and j.dep_ == "conj":
                            may_cont.add(j)
    return may_cont, ext, label


def might_perf_active(doc):
    might_perf_active = set()
    label = "might_perf"
    ext = "modal_verbs"

    for token in doc:
        if token.lemma_ == "might" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.subtree:
                if t.text == "have":
                    might_perf_active.add(head)
                    might_perf_active.add(t)

                    for k in head.children:
                        if k.text == "been" and k.dep_ != "ROOT" and (head in might_perf_active):
                            might_perf_active.remove(head)
                            might_perf_active.remove(t)

            if head in might_perf_active:
                might_perf_active.add(token)

            for j in head.subtree:
                if (j.tag_ == "VBN" or j.tag_ == "VBD") and j.dep_ == "conj":
                    might_perf_active.add(j)
    return might_perf_active, ext, label


def might_perf_passive(doc):
    might_perf_passive = set()
    label = "might_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "might" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.text == "been" and t.dep_ == "auxpass":
                    might_perf_passive.add(head)
                    might_perf_passive.add(token)
                    might_perf_passive.add(t)

                    for k in head.children:
                        if k.lemma_ == "have":
                            might_perf_passive.add(k)

            for k in head.subtree:
                if k.tag_ == "VBN" and k.dep_ == "conj" and head in might_perf_passive:
                    might_perf_passive.add(k)
    return might_perf_passive, ext, label


def may_perf_passive(doc):
    may_perf_passive = set()
    label = "might_perf_passive"
    ext = "modal_verbs"

    for token in doc:

        if token.lemma_ == "may" and token.head.tag_ == "VBN":
            head = token.head

            for t in head.children:
                if t.text == "been" and t.dep_ == "auxpass":
                    may_perf_passive.add(head)
                    may_perf_passive.add(token)
                    may_perf_passive.add(t)
                if t.lemma_ == "have":
                    may_perf_passive.add(t)

            for k in head.subtree:
                if k.tag_ == "VBN" and k.dep_ == "conj" and head in may_perf_passive:
                    may_perf_passive.add(k)
    return may_perf_passive, ext, label


"""ADJECTIVES AND ADVERBS: DEGREES OF COMPARISON"""


def adjectives(doc):
    adj = {}

    for token in doc:
        if "Degree=Pos" in token.morph and token.pos_ == "ADJ":
            adj[token] = "positive_adjective"

        if "Degree=Pos" in token.morph and token.pos_ == "ADJ":
            head = token
            for child in head.children:
                if "Degree=Cmp" in child.morph:
                    adj[head] = "comparative_adjective"
                    adj[child] = "comparative_adjective"

        if "Degree=Cmp" in token.morph and (token not in adj) and token.pos_ == "ADJ":
            adj[token] = "comparative_adjective"

        if "Degree=Pos" in token.morph and token.pos_ == "ADJ":
            head = token
            for child in head.children:
                if "Degree=Sup" in child.morph:
                    adj[head] = "superlative_adjective"
                    adj[child] = "superlative_adjective"

        if "Degree=Sup" in token.morph and token.tag_ == "JJS" and token.head.pos_ != "ADV":
            adj[token] = "superlative_adjective"

        if "Degree=Pos" in token.morph and token.pos_ == "ADJ":
            head = token
            for child in head.children:
                if "PunctType=Dash" in child.morph:
                    for t in head.children:
                        if t.pos_ == "ADJ":
                            adj[t] = "positive_adjective"
                        if t.dep_ == "advmod":
                            adj[t] = "positive_adjective"

        if token.dep_ == "acomp":
            for child in token.children:
                if "PunctType=Dash" in child.morph:
                    for t in token.children:
                        if t.pos_ == "ADV" or child.pos_ == "ADJ":
                            adj[token] = "positive_adjective"
                            adj[t] = "positive_adjective"

        if token.pos_ == "ADJ" and (token.head.pos_ == "VERB" or token.head.pos_ == "AUX") and token in adj:
            del adj[token]

        if token.pos_ == "ADJ" and (token.dep_ == "npadvmod" or token.dep_ == "advmod") and token in adj:
            del adj[token]

    return adj


def adverbs(doc):
    adv = {}

    for token in doc:
        if token.tag_ == "RB":
            adv[token] = "positive_adverb"

        if token.tag_ == "RB":
            head = token
            for child in head.children:
                if "Degree=Cmp" in child.morph and child.tag_ == "RBR":
                    adv[head] = "comparative_adverb"
                    adv[child] = "comparative_adverb"

        if "Degree=Cmp" in token.morph and (token not in adv) and token.tag_ == "RBR" and token.head.pos_ == "ADV":
            adv[token] = "comparative_adverb"

        if token.tag_ == "RB" and token.dep_ == "advmod":
            head = token
            for child in head.children:
                if "Degree=Sup" in child.morph and child.tag_ == "RBS":
                    adv[head] = "superlative_adverb"
                    adv[child] = "superlative_adverb"

        if "Degree=Sup" in token.morph and token.tag_ == "JJS" and token.head.pos_ == "ADV":
            adv[token] = "superlative_adjective"

        if "Degree=Sup" in token.morph and token.pos_ == "ADV":
            adv[token] = "superlative_adverb"

        if token.pos_ == "ADV":
            head = token
            for child in head.children:
                if "PunctType=Dash" in child.morph:
                    for t in head.children:
                        if t.pos_ == "ADV":
                            adv[t] = "positive_adverb"
                        if t.dep_ == "advmod":
                            adv[t] = "positive_adverb"

        if (token.pos_ == "ADJ" and "Degree=Sup" in token.morph) \
                and (token.dep_ == "npadvmod" or token.dep_ == "advmod"):
            adv[token] = "superlative_adverb"

    return adv


FUNCTION_LIST = [
    present_simple,
    present_ind_3p,
    present_cont,
    present_perfect_cont,
    present_ind_pas,
    present_cont_pas,
    present_perfect_passive,
    present_perfect,
    past_simple_passive,
    past_simple,
    past_simple_be,
    past_cont_passive,
    past_cont,
    past_perfect,
    past_perf_passive,
    past_perfect_cont,
    future_simple,
    future_simple_passive,
    future_cont,
    future_progr_passive,
    future_perfect,
    future_perfect_passive,
    future_perf_cont,
    would_ind_active,
    would_ind_passive,
    would_cont_active,
    would_perf_active,
    would_perf_passive,
    should_ind_active,
    should_ind_passive,
    shall_ind_active,
    shall_ind_passive,
    should_cont,
    should_perf_active,
    should_perf_passive,
    must_ind_active,
    must_cont,
    must_perf_active,
    must_perf_passive,
    can_ind,
    can_ind_passive,
    could_ind_active,
    could_ind_passive,
    can_cont,
    could_cont,
    could_perf_active,
    could_perf_passive,
    may_ind_active,
    may_ind_passive,
    might_ind_active,
    might_ind_passive,
    may_cont,
    might_perf_active,
    might_perf_passive,
    may_perf_passive,
]
