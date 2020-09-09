# -*- coding: utf-8 -*-
"""
@Author: Uzin
@Date: 2020-09-07
@Last Modified by: peviroy
@Last Modified time: 2020-09-09 9:20
"""
import sys
import os
sys.path.append(os.path.abspath(".."))
from dataset import get_sms_dataset
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV as gsc


def viewFrequency(df, column, cond):
    words = Counter()
    _words = df[df.loc[:, column] == cond].message.apply(
        lambda message: [word for word in message.split()])
    for word in _words:
        words.update(word)
    print(f'{column:s}-{cond}: ', words.most_common(50))

# k折调参 : 测试后显示折线图
# 参数:x_train, y_train,
#     begin，end,(测试范围)
#     delta(测试值的次数, 影响测试的精度)


def kf_test_and_draw(x_train, y_train, begin, end, test_num, name_scoring):
    alpha_range = np.linspace(begin, end, test_num)
    cv_scores = []  # 用来放每个模型的结果值
    for al in alpha_range:  # 用循环来测试每个alpha值对模型的影响
        nb = MultinomialNB(alpha=al, fit_prior=False)
        scores = cross_val_score(nb, x_train, y_train,
                                 cv=10, scoring=name_scoring)
        cv_scores.append(scores.mean())
    plt.plot(alpha_range, cv_scores)
    plt.xlabel('Alpha')
    plt.ylabel(name_scoring)
    plt.show()


'''
kf_test_and_draw(X_train, y_train, 0.1, 3.0, 20, "neg_mean_squared_error")
'''

# 调参 : 测试后控制台给出结果(最好的参数以及对应的数据)
# 参数:x_train, y_train,
#     begin，end,(测试范围)
#     delta(测试值的次数, 影响测试的精度)


def auto_test(x_data, y_data, begin, end, test_num, name_scoring):
    param_grid = [
        {'alpha': np.linspace(begin, end, test_num),
         'fit_prior': [True, False]},
    ]
    nb = MultinomialNB()
    # GridSearchCV
    grid = gsc(nb, param_grid, scoring=name_scoring)
    grid.fit(x_data, y_data)
    print(grid.best_params_, grid.best_score_)
    return float(grid.best_params_['alpha'])


'''
auto_test(X_train, y_train, 0.1, 10.0, 80, "neg_log_loss")
'''


def auto_test_for_other_model(model, param_grid, name_scoring):
    data_df = get_sms_dataset(noStopwords=True, overwrite=True)
    X, y = data_df['message'], data_df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.2)
    cv = CountVectorizer()
    X_train = cv.fit_transform(X_train)
    grid = gsc(model, param_grid, scoring=name_scoring)
    grid.fit(X_train, y_train)
    print(grid.best_params_, grid.best_score_)
    return grid.best_params_, grid.best_score_


def kf_test_with_datas(begin, end, test_num, name_scoring="neg_mean_squared_error"):
    data_df = get_sms_dataset(noStopwords=True, overwrite=True)
    X, y = data_df['message'], data_df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.2)
    cv = CountVectorizer()
    X_train = cv.fit_transform(X_train)
    kf_test_and_draw(X_train, y_train, begin, end, test_num, name_scoring)


'''
kf_test_with_datas(0.1, 1.3, 50)
'''


def auto_test_with_datas(begin, end, test_num, name_scoring="neg_mean_squared_error"):
    data_df = get_sms_dataset(noStopwords=True, overwrite=True)
    X, y = data_df['message'], data_df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.2)
    cv = CountVectorizer()
    X_train = cv.fit_transform(X_train)
    auto_test(X_train, y_train, begin, end, test_num, name_scoring)


'''
auto_test_with_datas(0.1, 1.3, 50)
'''


def kf_test_with_datas_and_draw_alot(begin, end, test_num):
    data_df = get_sms_dataset(noStopwords=True, overwrite=True)
    X, y = data_df['message'], data_df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.2)
    cv = CountVectorizer()
    X_train = cv.fit_transform(X_train)
    kf_test_and_draw(X_train, y_train, begin, end, test_num, 'accuracy')
    kf_test_and_draw(X_train, y_train, begin, end, test_num, 'precision')
    kf_test_and_draw(X_train, y_train, begin, end, test_num, 'f1')
    kf_test_and_draw(X_train, y_train, begin, end, test_num, 'recall')


'''
kf_test_with_datas_and_draw_alot(0.1, 1.3, 200)
'''
