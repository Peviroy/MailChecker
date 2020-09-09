"""
@Author: Uzin
@Date: 2020-09-07
@Last Modified by: peviroy
@Last Modified time: 2020-09-09 9:20
"""
import sys
import os
sys.path.append(os.path.abspath(".."))
from utils.preprocessing import TextPurifier

import utils.test_tool as test_tool
from dataset import get_sms_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib
import pickle

# 对NB模型训练一次


class MultiNB_Wrapper():
    def __init__(self):
        super().__init__()

    def train_once(self, x_data, y_data, alpha):
        nb = MultinomialNB(alpha)
        nb.fit(x_data, y_data)
        return nb

    def generate_model(self, scoring="precision"):
        data_df = get_sms_dataset(noStopwords=True, overwrite=True)
        X, y = data_df['message'], data_df['target']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=0, test_size=0.2)
        cv = CountVectorizer()
        X_train = cv.fit_transform(X_train)
        bp = test_tool.auto_test(X_train, y_train, 0.1, 1.5, 200, scoring)

        nb = self.train_once(X_train, y_train, bp)
        self.save_model(nb, cv)
        return nb

    def get_params(self):
        model = self.load_model()
        return model

    def save_model(self, model, cv, save_mode="pickle", model_name="model", cv_name="cv"):
        if save_mode == 'pickle':
            # print("pickle")
            with open(model_name + '.pickle', 'wb') as f:
                pickle.dump(model, f)
            with open(cv_name + '.pickle', 'wb') as f:
                pickle.dump(cv, f)
        elif save_mode == 'joblib':
            # print("joblib")
            joblib.dump(model, model_name + '.model')
            joblib.dump(cv, cv_name + '.pkl')
        else:
            print("plz input correct save_mode")

    def load_model(self, save_mode="pickle", model_name="model", cv_name="cv"):
        if save_mode == 'pickle':
            # print("pickle")
            with open('model.pickle', 'rb') as f:
                model = pickle.load(f)
            with open('cv.pickle', 'rb') as f:
                cv = pickle.load(f)
            return model, cv
        elif save_mode == 'joblib':
            # print("joblib")
            joblib.load(model, model_name + '.model')
            joblib.load(cv, cv_name + '.pkl')
            return model, cv
        else:
            print("plz input correct save_mode")

    def predict(self, text):
        model, cv = self.load_model()
        text_purified = self.get_vector_from_text(text)
        pred = model.predict(cv.transform(text_purified))
        proba = model.predict_proba(cv.transform(text_purified))
        # print(pred)
        return pred, proba

    def get_alpha(self):
        return self.load_model().alpha

    def get_vector_from_text(self, text):
        text_purified = TextPurifier(texts=[text]).purify()
        return text_purified
