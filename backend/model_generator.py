import os
from model.LSTM_Wrapper import LSTM_Wrapper
import numpy as np
import torch


class LSTMG_Controller:
    def __init__(self, model_type='model_spam'):
        device = torch.device('cpu')
        word_dict_path, embed_layer_path, model_path = self._load_checkpoints(
            model_type=model_type)
        self.word_dict = np.load(
            word_dict_path, allow_pickle=True).item()

        self.index_dict = {item[1]: item[0]
                           for item in self.word_dict.items()}

        self.model_wrapper = LSTM_Wrapper(device=device,
                                          word_dict=self.word_dict, index_dict=self.index_dict, pre_file_path=embed_layer_path)
        self.model_wrapper.fit()
        self.model_wrapper.load_model(device=device, full_path=model_path)

    def predict(self, text, nextwords=50):
        words = self.model_wrapper.predict([text], nextwords=nextwords)
        if words is None:
            return 'Some word not contained, change another mail or nextwords'
        text = ' '.join(words)
        return text

    def _load_checkpoints(self, dir_path='../checkpoints/', model_type='model_ham'):
        WORD_DICT_NAME = 'word_dict.npy'
        EMBEDDING_NAME = 'glove100.npy'
        MODEL_NAME = 'model_final'

        word_dict_path = os.path.join(
            dir_path, model_type, WORD_DICT_NAME
        )
        embed_layer_path = os.path.join(
            dir_path, model_type, EMBEDDING_NAME
        )
        model_path = os.path.join(
            dir_path, model_type, MODEL_NAME
        )
        return word_dict_path, embed_layer_path, model_path


if __name__ == "__main__":
    lgc = LSTMG_Controller()
    lgc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent')
