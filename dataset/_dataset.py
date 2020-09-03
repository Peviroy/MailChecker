"""
@Author: peviroy
@Date: 2020-09-02
@Last Modified by: peviroy
@Last Modified time: 2020-09-03 00:10
"""

import pandas as pd
import os
from utils.preprocessing import TextPurifier

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_sms_dataset(raw=False, SMS_DATASET='data/spam.csv'):
    '''
    Prepare dataset. do something trivial but necessary.
    Argument:
        raw {boolean} -- processing dataset or return directly
    '''

    SMS_DATASET_PATH = os.path.join(BASE_DIR, SMS_DATASET)
    if raw is True:
        if not os.path.exists(SMS_DATASET_PATH):
            raise FileNotFoundError('Cannot find data/spam.csv')
        return pd.read_csv(SMS_DATASET_PATH, encoding="latin-1")
    else:
        SMS_PURIFIED_DATASET_PATH = SMS_DATASET_PATH.replace(
            'spam.csv', 'spam_purified.csv')
        if os.path.exists(SMS_PURIFIED_DATASET_PATH):
            return pd.read_csv(SMS_PURIFIED_DATASET_PATH, encoding="latin-1")
        else:
            return _purify_sms_dataset(get_sms_dataset(raw=True, SMS_DATASET=SMS_DATASET))


def _purify_sms_dataset(data_df):
    '''
    Purify sms_dataset. Helper of get_sms_dataset
    Argument:
        data_df {DataFrame} -- data of sms_dataset in the form of pandas.DataFrame
    '''
    # remove unnecessary features
    data_df = data_df.drop(columns=data_df.columns[2:5])

    # rename columns
    data_df = data_df.rename(columns={'v1': 'target', 'v2': 'message'})

    # encode labels|targets to integer
    data_df['target'] = data_df['target'].map({'ham': 0, 'spam': 1})

    # purify texts
    data_df['message'] = TextPurifier(
        texts=data_df['message'].to_list()).purify()

    data_df.to_csv(os.path.join(
        BASE_DIR, 'data/spam_purified.csv'), index=False, encoding="latin-1")
    return data_df
