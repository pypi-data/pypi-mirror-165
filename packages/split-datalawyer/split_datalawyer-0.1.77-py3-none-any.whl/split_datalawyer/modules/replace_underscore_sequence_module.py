import re

from split_datalawyer.modules import ModulesType


class ReplaceUnderscoreSequenceModule:

    def get_type(self):
        return ModulesType.REPLACE

    def transform(self, text):
        underscore_sequences = re.findall(r"\_{2,}", text)

        for sequence in underscore_sequences:
            text = re.sub(sequence, f" {sequence} ", text)

        return text
