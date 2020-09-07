"""
@Author: peviroy
@Date: 2020-09-03 20:11
@Last Modified by: peviroy
@Last Modified time: 2020-09-06 21:06
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))

from dataset import get_sms_dataset
from utils.preprocessing import TextPurifier


class TestSMSInstance:
    def test_null_raw_file(self):
        try:
            get_sms_dataset(raw=True, SMS_DATASET='null')
        except Exception as e:
            assert isinstance(e, FileNotFoundError)

    def test_raw_file(self):
        assert get_sms_dataset(
            raw=True) is not None

    def test_purified_file(self):
        data_df = get_sms_dataset(
            raw=False)
        assert data_df is not None
        # confirm purified
        for rule_name, matched in TextPurifier(texts=data_df['message']).show_iter():
            print(matched)
            assert matched == []
