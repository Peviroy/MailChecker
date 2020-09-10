from model.BiLSTM_Wrapper import BiLSTM_Wrapper
import numpy as np
import os


def load_module():
    model_wrapper = BiLSTM_Wrapper(word_dict=_load_word_dict())
    model_wrapper.fit()
    return model_wrapper


def _load_word_dict():
    WORD_DICT_DIR = './checkpoints'
    WORD_DICT_NAME = 'word_dict.npy'
    word_dict_path = os.path.join(WORD_DICT_DIR, WORD_DICT_NAME)
    try:
        word_dict = np.load(
            word_dict_path, allow_pickle=True).item()
    except FileNotFoundError:
        raise FileExistsError('word dict must be specified')
    return word_dict
