import re

from split_datalawyer.modules import ModulesType


class ReplaceUnderscoreSequenceModule:

    def get_type(self):
        return ModulesType.REPLACE

    def transform(self, text):
        # underscore_sequences = sorted(set(re.findall(r"\_{2,}", text)), key=len, reverse=True)
        #
        # for sequence in underscore_sequences:
        #     text = text.replace(sequence, f" {sequence} ")
        #
        # return text

        underscore_pattern = re.compile(r"\_{2,}")
        text = re.sub(underscore_pattern, " __ ", text)
        dot_pattern = re.compile(r"\.{2,}")
        text = re.sub(dot_pattern, " .. ", text)
        return text
