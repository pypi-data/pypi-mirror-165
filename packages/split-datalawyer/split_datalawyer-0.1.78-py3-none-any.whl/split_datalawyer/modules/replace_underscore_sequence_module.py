import re

from split_datalawyer.modules import ModulesType


class ReplaceUnderscoreSequenceModule:

    def get_type(self):
        return ModulesType.REPLACE

    def transform(self, text):
        underscore_sequences = sorted(set(re.findall(r"\_{2,}", text)), key=len, reverse=True)

        for sequence in underscore_sequences:
            text = text.replace(sequence, f" {sequence} ")

        return text
