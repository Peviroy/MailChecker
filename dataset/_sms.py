"""
@Author: peviroy
@Date: 2020-09-02
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 23:07
"""

import pandas as pd
import os
from utils.preprocessing import TextPurifier

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_sms_dataset(raw=False, SMS_DATASET='data/spam.csv', type='all', noStopwords=False, overwrite=False):
    '''
    Prepare dataset. do something trivial but necessary.
    Argument:
        raw {boolean} -- processing dataset or return directly
                      -- raw for reserved only! dont use it to train
        noStopwords {Boolean} -- whether to purify stopwords or not
        overwrite {Boolean} -- get from a new data file or from a existing file
    '''

    SMS_DATASET_PATH = os.path.join(BASE_DIR, SMS_DATASET)
    if raw is True:
        if not os.path.exists(SMS_DATASET_PATH):
            raise FileNotFoundError('Cannot find data/spam.csv')
        return pd.read_csv(SMS_DATASET_PATH, encoding="latin-1")
    else:
        SMS_PURIFIED_DATASET_PATH = SMS_DATASET_PATH.replace(
            'spam.csv', 'spam_purified_withstop.csv')
        if os.path.exists(SMS_PURIFIED_DATASET_PATH) and not overwrite:
            data_df = pd.read_csv(
                SMS_PURIFIED_DATASET_PATH, encoding="latin-1")
        else:
            data_df = _purify_sms_dataset(get_sms_dataset(raw=True, SMS_DATASET=SMS_DATASET, noStopwords=noStopwords,
                                                          overwrite=overwrite), noStopwords=noStopwords, if_save_path=SMS_PURIFIED_DATASET_PATH)
        if type == 'ham':
            data_df = data_df[data_df['target'] == 0]
        elif type == 'spam':
            data_df = data_df[data_df['target'] == 1]
        data_df['length'] = data_df['message'].map(len)
        return data_df


def _purify_sms_dataset(data_df, noStopwords, if_save_path):
    '''
    Purify sms_dataset. Helper of get_sms_dataset
    Argument:
        data_df {DataFrame} -- data of sms_dataset in the form of pandas.DataFrame
        noStopwords {Boolean} -- whether to purify stopwords or not
    '''
    # remove unnecessary features
    data_df = data_df.drop(columns=data_df.columns[2:5])

    # rename columns
    data_df = data_df.rename(columns={'v1': 'target', 'v2': 'message'})

    # encode labels|targets to integer
    data_df['target'] = data_df['target'].map({'ham': 0, 'spam': 1})

    # purify texts
    data_df['message'] = TextPurifier(
        texts=data_df['message'].to_list(), noStopwords=noStopwords).purify()

    data_df.to_csv(if_save_path, index=False, encoding="latin-1")
    return data_df
