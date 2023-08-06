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
import itertools

from stylo_metrix.metrics.en.en import EnglishMetric
from stylo_metrix.structures import MetricsGroup
from stylo_metrix.utils import incidence, ratio, start_end_quote
from spacy.tokens import Span


class Syntactic(EnglishMetric, ABC):
    category_en = "Syntactic"
    category_id = 5


class SY_QUESTION(Syntactic):
    name_en = "Words in questions incidence"
    metric_id = 1

    def count(self, doc):
        sentence_tokens = [[token for token in sent if '?' in sent.text] for sent in doc.sents]
        words = sum([[token for token in sent if token._.is_word] for sent in sentence_tokens], [])
        result = incidence(doc, words)
        return result, {"QS": sentence_tokens}


class SY_EXCLAMATION(Syntactic):
    name_en = "Words in exclamatory sentences incidence"
    metric_id = 2

    def count(self, doc):
        sentence_tokens = [[token for token in sent if '!' in sent.text] for sent in doc.sents]
        words = sum([[token for token in sent if token._.is_word] for sent in sentence_tokens], [])
        result = incidence(doc, words)
        return result, {}


class SY_IMPERATIVE(Syntactic):
    name_en = "Words in imperative sentences incidence"
    metric_id = 3

    def count(self, doc):
        sentence_tokens = [[token for token in sent] for sent in doc.sents if
                           "VerbForm=Inf" in sent[0].morph and sent[0].pos_ == "VERB"]
        words = sum([[token for token in sent if token._.is_word] for sent in sentence_tokens], [])
        result = incidence(doc, words)
        return result, {}


class SY_SUBORD_SENT(Syntactic):
    name_en = "Words in subordinate sentences incidence"
    metric_id = 4

    def count(self, doc):
        subord_sentences = [sent for sent in doc.sents if any(token.pos_ == "SCONJ" for token in sent)]
        join_sents = itertools.chain(*subord_sentences)
        sent_tok = [tkn for tkn in join_sents if tkn.pos_ != "PUNCT"]

        result = incidence(doc, sent_tok)
        return result, {"SUBORD_SENT": sent_tok}


class SY_SUBORD_SENT_PUNCT(Syntactic):
    name_en = "Punctuation in subordinate sentences incidence"
    metric_id = 5

    def count(self, doc):
        sub_sent_punct = [sent for sent in doc.sents if any(token.pos_ == "SCONJ" for token in sent)]
        join_sents = itertools.chain(*sub_sent_punct)
        sent_tok = [tkn for tkn in join_sents if tkn.pos_ in "PUNCT"]

        result = incidence(doc, sent_tok)
        return result, {"SUBORD_SENT_PUNCT": sent_tok}


class SY_COORD_SENT(Syntactic):
    name_en = "Words in coordinate sentences incidence"
    metric_id = 6

    def count(self, doc):
        coord_sentences = [sent for sent in doc.sents if any(token.pos_ == "CCONJ" for token in sent)]
        join_sents = itertools.chain(*coord_sentences)
        sent_tok = [tkn for tkn in join_sents if tkn.pos_ != "PUNCT"]

        result = incidence(doc, sent_tok)
        return result, {"COORD": sent_tok}


class SY_COORD_SENT_PUNCT(Syntactic):
    name_en = "Punctuation in coordinate sentences incidence"
    metric_id = 7

    def count(self, doc):
        coord_sent_punct = [sent for sent in doc.sents if any(token.pos_ == "CCONJ" for token in sent)]
        join_sents = itertools.chain(*coord_sent_punct)
        sent_tok = [tkn for tkn in join_sents if tkn.pos_ in "PUNCT"]

        result = incidence(doc, sent_tok)
        return result, {"COORD_PUNCT": sent_tok}


class SY_SIMPLE_SENT(Syntactic):
    name_en = "Tokens in simple sentences incidence"
    metric_id = 8

    def count(self, doc):
        sentence_tokens = [[sent for token in sent if token.pos_ == "SCONJ" or token.pos_ == "CCONJ"] for sent in
                           doc.sents]
        flattened = [val for sublist in sentence_tokens for val in sublist]
        simple_sent = [[token for token in sent] for sent in doc.sents if
                       sent not in flattened]
        flattened_simple = [val for sublist in simple_sent for val in sublist]

        result = incidence(doc, flattened_simple)
        return result, {}


class SY_DIRECT_SPEECH(Syntactic):
    name_en = "Number of words in direct speech"
    metric_id = 9

    def count(self, doc):
        start, end = start_end_quote(doc)
        if (start and end) != None:
            span = doc[start:end]
            span_words = [token for token in span]
            result = incidence(doc, span_words)
            return result, {"Direct Speech": span_words}
        else:
            result = ratio(len(doc), 0)
            return result, {}


SYNTACTIC = [
    SY_QUESTION,
    SY_EXCLAMATION,
    SY_IMPERATIVE,
    SY_SUBORD_SENT,
    SY_SUBORD_SENT_PUNCT,
    SY_COORD_SENT,
    SY_COORD_SENT_PUNCT,
    SY_SIMPLE_SENT,
    SY_DIRECT_SPEECH,
]

syntactic_group = MetricsGroup([m() for m in SYNTACTIC])
