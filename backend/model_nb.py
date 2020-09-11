import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))
from model.MultiNB import MultiNB_Wrapper
import os


class MultiNB_Controller:
    def __init__(self):
        self.model_wrapper = MultiNB_Wrapper()

    def predict(self, text):
        predict, prob = self.model_wrapper.predict(text)
        if predict[0] == 0:
            predict = 'ham'
        else:
            predict = 'spam'
        prob = prob[0][0]
        print(predict)
        print(prob)
        return predict, prob


if __name__ == "__main__":
    bc = MultiNB_Controller()
    bc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent')
