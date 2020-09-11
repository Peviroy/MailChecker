"""
@Author: Uzin
@Date: 2020-09-07
@Last Modified by: peviroy
@Last Modified time: 2020-09-09 9:20
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))
from utils.preprocessing import TextPurifier
import utils.test_tool as test_tool
from dataset import get_sms_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib
import pickle
from scipy.sparse import csr_matrix, hstack
from sklearn import metrics


class MultiNB_Wrapper():
    def __init__(self):
        super().__init__()

    @staticmethod
    def train_once(x_data, y_data, alpha):
        nb = MultinomialNB(alpha)
        nb.fit(x_data, y_data)

        return nb

    @staticmethod
    def generate_model(scoring="precision"):
        data_df = get_sms_dataset(noStopwords=True, overwrite=True)
        X, y = data_df['message'], data_df['target']

        cv = CountVectorizer()
        X = cv.fit_transform(X)
        lens = data_df['length']
        new_len = csr_matrix(lens)
        X = hstack((X, new_len.reshape(-1, 1)))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=0, test_size=0.2)
        bp = test_tool.auto_test(X_train, y_train, 0.1, 1.5, 200, scoring)

        nb = MultiNB_Wrapper.train_once(X_train, y_train, bp)

        MultiNB_Wrapper.save_model(nb, cv)

        pred = nb.predict(X_test)
        print(metrics.confusion_matrix(y_test, pred))
        return nb

    @staticmethod
    def generate_model_no_length(scoring="accuracy"):
        data_df = get_sms_dataset(noStopwords=True, overwrite=True)
        X, y = data_df['message'], data_df['target']

        cv = CountVectorizer()
        X = cv.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=0, test_size=0.2)
        bp = test_tool.auto_test(X_train, y_train, 0.1, 1.5, 200, scoring)

        nb = MultiNB_Wrapper.train_once(X_train, y_train, bp)
        MultiNB_Wrapper.save_model(
            nb, cv, model_name='old_model', cv_name="old_cv")

        pred = nb.predict(X_test)
        print(metrics.confusion_matrix(y_test, pred))
        return nb

    @staticmethod
    def save_model(model, cv, save_mode="pickle", model_name="model", cv_name="cv"):
        if save_mode == 'pickle':
            # print("pickle")
            with open(model_name + '.pickle', 'wb') as f:
                pickle.dump(model, f)
            with open(cv_name + '.pickle', 'wb') as f:
                pickle.dump(cv, f)
            return model_name + '.pickle'
        elif save_mode == 'joblib':
            # print("joblib")
            joblib.dump(model, model_name + '.model')
            joblib.dump(cv, cv_name + '.pkl')
            return model_name + '.model'
        else:
            print("plz input correct save_mode")

    @staticmethod
    def load_model(load_path='../checkpoints/model_nb/', save_mode="pickle", model_name="model", cv_name="cv"):
        if save_mode == 'pickle':
            # print("pickle")
            with open(load_path + model_name + '.pickle', 'rb') as f:
                model = pickle.load(f)
            with open(load_path + cv_name + '.pickle', 'rb') as f:
                cv = pickle.load(f)
            return model, cv
        elif save_mode == 'joblib':
            # print("joblib")
            model = joblib.load(load_path + model_name + '.model')
            cv = joblib.load(load_path + cv_name + '.pkl')
            print('ok load')
            return model, cv
        else:
            print("plz input correct save_mode")

    @staticmethod
    def predict(text):
        model, cv = MultiNB_Wrapper.load_model()
        text_purified = MultiNB_Wrapper.get_vector_from_text(text)
        lens = len(text_purified)

        temp = cv.transform(text_purified)

        new_len = csr_matrix(lens)
        temp = hstack((temp, new_len.reshape(-1, 1)))

        pred = model.predict(temp)
        proba = model.predict_proba(temp)
        # print(pred)
        return pred, proba

    @staticmethod
    def get_alpha():
        out_files = MultiNB_Wrapper.load_model()
        return out_files[0].alpha

    @staticmethod
    def get_vector_from_text(text):
        text_purified = TextPurifier(texts=[text]).purify()
        return text_purified
