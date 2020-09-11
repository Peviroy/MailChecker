from model.BiLSTM_Wrapper import BiLSTM_Wrapper
import numpy as np
import torch
import os


class BILSTM_Controller:
    def __init__(self):
        device = torch.device('cpu')
        word_dict_path, embed_layer_path, model_path = self._load_checkpoints()
        self.word_dict = np.load(
            word_dict_path, allow_pickle=True).item()
        self.model_wrapper = BiLSTM_Wrapper(device=device,
                                            word_dict=self.word_dict, pre_file_path=embed_layer_path)
        self.model_wrapper.fit()
        self.model_wrapper.load_model(device=device, full_path=model_path)

    def predict(self, text):
        predict, imgpath = self.model_wrapper.predict([text])
        if predict[0] == 0:
            predict = 'ham'
        else:
            predict = 'spam'
        print(predict)
        print(imgpath)
        return predict, imgpath

    def _load_checkpoints(self, dir_path='../checkpoints/bilstm'):
        WORD_DICT_NAME = 'word_dict.npy'
        EMBEDDING_NAME = 'glove100.npy'
        MODEL_NAME = 'model_final'

        word_dict_path = os.path.join(
            dir_path, WORD_DICT_NAME
        )
        embed_layer_path = os.path.join(
            dir_path, EMBEDDING_NAME
        )
        model_path = os.path.join(
            dir_path, MODEL_NAME
        )
        return word_dict_path, embed_layer_path, model_path


if __name__ == "__main__":
    bc = BILSTM_Controller()
    bc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent')
