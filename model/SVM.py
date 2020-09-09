# -*- coding: utf-8 -*-
"""
@Author: Uzin
@Date: 2020-09-07
@Last Modified by: peviroy
@Last Modified time: 2020-09-09 9:20
"""

import numpy as np
from sklearn.svm import LinearSVC
import utils.test_tool as test_tool
import sys
import os
sys.path.append(os.path.abspath(".."))
from dataset import get_sms_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


def train_SVM(x_data, y_data, penalty='l2', loss='squared_hinge', dual=True, C=1.0, multi_class='ovr', fit_intercept=True, intercept_scaling=1):
    svc = LinearSVC(penalty=penalty, loss=loss, dual=dual, C=C, multi_class=multi_class,
                    fit_intercept=fit_intercept, intercept_scaling=intercept_scaling)
    svc.fit(x_data, y_data)
    return svc


def do_SVM_test():
    param_grid = [
        {'penalty': ['l1', 'l2'], 'loss': ['hinge', 'squared_hinge'], 'dual': [
            True, False], 'C': np.linspace(0.9, 1.0, 20), 'multi_class': ['ovr', 'crammer_singer']}
    ]

    svc = LinearSVC()
    test_tool.auto_test_for_other_model(svc, param_grid, 'accuracy')


data_df = get_sms_dataset(noStopwords=True, overwrite=True)
X, y = data_df['message'], data_df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=0, test_size=0.2)
cv = CountVectorizer()
X_train = cv.fit_transform(X_train)
train_SVM(X_train, y_train)
