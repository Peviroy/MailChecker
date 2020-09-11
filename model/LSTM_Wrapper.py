"""
@Author: peviroy
@Date: 2020-09-09
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 22:00
"""
import os
import time
import torch
import numpy as np

from utils.preprocessing import TextPurifier
from utils.Meter import AverageMeter, ProgressMeter
from .LSTM import LSTM_Generator


class LSTM_Wrapper:
    '''
    A union for a series of operations of BiLSTM. e.g. data transform, train, predict...
    '''

    def __init__(self, device, word_dict, index_dict, pre_file_path=None):
        '''
        Empty wrapper created, use 'fit and train' to start train a new model or use 'load' to get a pretrained model
        '''
        super(LSTM_Wrapper, self).__init__()
        self.device = device
        self.word_dict = word_dict
        self.index_dict = index_dict
        self.pre_file_path = pre_file_path

    def fit(self, **args):
        self._vocab_size = len(self.word_dict)
        n_hidden = args.get('n_hidden') or 128
        embeddings_matrix = self._get_glove_embedding(
            checkpoint_path=self.pre_file_path)
        self.model = LSTM_Generator(
            self.device, self._vocab_size, n_hidden=n_hidden, embedding_dim=100, embedding_matrix=embeddings_matrix)
        self.model = self.model.to(self.device)

    def _get_glove_embedding(self, **args):
        FILE_PATH = args.get('file_path') or 'data/glove.6B.100d.txt'
        if args.get('checkpoint_path') is not None:
            if os.path.isfile(args.get('checkpoint_path')):
                CHECKPOINT_PATH = str(args.get(
                    'checkpoint_path'))
            else:
                CHECKPOINT_PATH = str(args.get(
                    'checkpoint_path')) + 'glove100.npy'
        else:
            CHECKPOINT_PATH = 'checkpoints/glove100.npy'

        if not os.path.exists(FILE_PATH) and not os.path.isfile(CHECKPOINT_PATH):
            raise FileExistsError('Glove file not founded')
        if os.path.exists(CHECKPOINT_PATH):
            embeddings_matrix = np.load(CHECKPOINT_PATH)
        else:
            embeddings_index = dict()
            with open(FILE_PATH) as file:
                for line in file:
                    values = line.split()
                    word = values[0]
                    coefs = np.asarray(values[1:], dtype='float32')
                    embeddings_index[word] = coefs
            embeddings_matrix = np.zeros((self._vocab_size + 1, 100))
            np.save(CHECKPOINT_PATH, embeddings_matrix)
            for word, i in self.word_dict.items():
                embedding_vector = embeddings_index.get(word)
                if embedding_vector is not None:
                    embeddings_matrix[i] = embedding_vector
        return embeddings_matrix

    def train(self, trainloader, criterion, optimizer, state_h, state_c, current_epoch=0):
        batch_time = AverageMeter(name='Time', fmt=':6.3f')
        losses = AverageMeter('Loss', ':.4e')
        progress = ProgressMeter(   # log
            len(trainloader),
            [batch_time, losses],
            prefix="[Train] Epoch: [{}]".format(current_epoch + 1))

        # train mode
        self.model.train()
        state_h = state_h.to(self.device)
        state_c = state_c.to(self.device)

        end = time.time()
        for batch_cnt, batch_data in enumerate(trainloader):
            # move into specific device
            text_batch_x, text_batch_y = batch_data
            text_batch_x, text_batch_y = text_batch_x.to(
                self.device), text_batch_y.to(self.device)

            # output
            y_pred, (state_h, state_c) = self.model(
                text_batch_x, (state_h, state_c))

            # calculate loss
            loss = criterion(y_pred.transpose(1, 2), text_batch_y)

            state_h = state_h.detach()
            state_c = state_c.detach()

            # detach makes no grad,
            losses.update(loss.detach().item(), n=text_batch_x.size(0))

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            # display
            progress.display(batch_cnt + 1)
        return losses.avg, progress.get(batch_cnt + 1)

    def predict(self, text: list, nextwords):
        '''
        Argument:
            text {list} -- list contains one string
        '''
        text = TextPurifier(text, noStopwords=False).purify()
        words = text[0].split(' ')

        state_h, state_c = self.model.init_state(len(words))
        state_h, state_c = state_h.to(self.device), state_c.to(self.device)

        with torch.no_grad():
            for i in range(0, nextwords):
                try:
                    x = torch.tensor([[self.word_dict[w]
                                       for w in words[i:]]]).to(self.device)
                except KeyError:
                    return None
                y_pred, (state_h, state_c) = self.model(x, (state_h, state_c))

                last_word_logits = y_pred[0][-1]
                p = torch.nn.functional.softmax(
                    last_word_logits, dim=0).detach().cpu().numpy()
                word_index = np.random.choice(len(last_word_logits), p=p)
                words.append(self.index_dict[word_index])

        return words

    def save_model(self, full_path: str):
        '''
        Argument:
            full_path {str} -- it's recommended to use formatted string to forms path
                            -- '{0:s}/model_{1:03d}_{2:.3f}'.format(MODEL_FOLDER, epoch+1, acc1)
        '''
        torch.save(self.model.state_dict(), full_path)

    def load_model(self, device, full_path: str, ):
        self.model.load_state_dict(torch.load(
            full_path, map_location=device
        ))
