import os
from model.MultiNB import MultiNB_Wrapper


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

        return predict, prob


if __name__ == "__main__":
    nbc = MultiNB_Controller()
    nbc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent')
