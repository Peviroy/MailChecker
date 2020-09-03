"""
@Author: peviroy
@Date: 2020-09-03 20:54
@Last Modified by: peviroy
@Last Modified time: 2020-09-03 21:07
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))

from dataset import get_sms_dataset
from utils.preprocessing import TextPurifier

raw_texts = get_sms_dataset(raw=True)['v2'].tolist()
tp = TextPurifier(raw_texts)


class TestTextPurifierInstance:
    def test_str(self):
        assert tp.__str__().startswith('Name:')

    def test_iter(self):
        for rule_name, matched_strings in tp.show_iter():
            assert matched_strings != []

    def test_purify(self):
        purifed_texts = tp.purify()
        tp.set_texts(purifed_texts)
        for rule_name, matched_strings in tp.show_iter():
            assert matched_strings == []
