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


import logging
from spacy.language import Language
from spacy.tokens import Doc
from stylo_metrix.structures.errors import LanguageNotImplemented, FileFailedError

log = logging.getLogger(__name__)


@Language.factory("stylo_metrix")
class StyloMetrixPipe:
    name_count = 0

    def __init__(self, nlp, name):
        lang = nlp.config["nlp"]["lang"]

        if lang == "pl":
            from stylo_metrix.pipeline.pl import COMPONENTS
        elif lang == "en":
            from stylo_metrix.pipeline.en import COMPONENTS
            from stylo_metrix.pipeline.en.custom_preprocessing import CustomPreprocessing
            nlp.tokenizer = CustomPreprocessing(nlp.tokenizer)
        else:
            raise LanguageNotImplemented()

        self.components = [component(nlp) for component in COMPONENTS]
        Doc.set_extension("name", default=None, force=True)
        Doc.set_extension("assign_name", method=self.assign_name, force=True)

    def __call__(self, doc):
        doc._.set("name", f"SM{StyloMetrixPipe.name_count:06d}")
        StyloMetrixPipe.name_count += 1

        try:
            for component in self.components:
                doc = component(doc)
        except Exception as e:
            log.error(e, exc_info=True)
            raise FileFailedError()

        return doc

    def assign_name(self, doc, name):
        doc._.name = name
        return doc
