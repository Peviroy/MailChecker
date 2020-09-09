"""
@Author: Hwan Jung(Jeff Jung) @graykode
@Date: 2020-08-14
@Last Modified by: peviroy
@Last Modified time: 2020-09-09 00:30
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))


from dataset import SMSDataset
import utils.random as urandom
MODEL_FOLDER = '../checkpoints'

minist_loss = 100000000


class BiLSTM_Attention(nn.Module):
    def __init__(self, vocab_size, n_hidden, num_classes, embedding_dim, embedding_matrix=None):
        '''
        Arguments:
            vocab_size      {int} -- vocabulary size
            n_hidden        {int} -- hidden_layers of LSTM
            embedding_dim   {int} -- dimension of word vector through embedding layer
            embedding_matrix{np.array} -- pretrained embeddinglayer weights
            num_classes     {int} -- predicted class num
        '''
        super(BiLSTM_Attention, self).__init__()
        self.n_hidden = n_hidden

        if embedding_matrix is None:
            self.embedding = nn.Embedding(vocab_size, embedding_dim)
        else:  # pretrained
            self.embedding = nn.Embedding.from_pretrained(
                torch.FloatTensor(embedding_matrix), freeze=True)

        self.lstm = nn.LSTM(embedding_dim, n_hidden, bidirectional=True)
        self.out = nn.Linear(n_hidden * 2, num_classes)

    # lstm_output : [batch_size, n_step==len_seq, n_hidden * num_directions(=2)], F matrix
    def attention_net(self, lstm_output, final_state):
        # hidden : [batch_size, n_hidden * num_directions(=2), 1(=n_layer)]
        hidden = final_state.view(-1, self.n_hidden * 2, 1)
        # attn_weights : [batch_size, n_step]
        attn_weights = torch.bmm(lstm_output, hidden).squeeze(2)
        soft_attn_weights = F.softmax(attn_weights, 1)
        # [batch_size, n_hidden * num_directions(=2), n_step] * [batch_size, n_step, 1] = [batch_size, n_hidden * num_directions(=2), 1]
        context = torch.bmm(lstm_output.transpose(
            1, 2), soft_attn_weights.unsqueeze(2)).squeeze(2)
        # context : [batch_size, n_hidden * num_directions(=2)]
        return context, soft_attn_weights.data.numpy()

    def forward(self, X):
        # input : [batch_size, len_seq, embedding_dim]
        input = self.embedding(X)
        # input : [len_seq, batch_size, embedding_dim]
        input = input.permute(1, 0, 2)

        # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        hidden_state = torch.zeros(1 * 2, len(X), self.n_hidden)
        # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        cell_state = torch.zeros(1 * 2, len(X), self.n_hidden)

        # output : [len_seq, batch_size, n_hidden]
        output, (final_hidden_state, final_cell_state) = self.lstm(
            input, (hidden_state, cell_state))
        # output : [batch_size, len_seq, n_hidden]
        output = output.permute(1, 0, 2)
        attn_output, attention = self.attention_net(output, final_hidden_state)
        # self.out(.) : [batch_size, num_classes], attention : [batch_size, n_step]
        return self.out(attn_output), attention


class BiLSTM_Wrapper:
    '''
    A union for a series of operations of BiLSTM. e.g. data transform, train, predict...
    '''

    def __init__(self):
        '''
        Empty wrapper created, use 'fit and train' to start train a new model or use 'load' to get a pretrained model
        '''
        super(BiLSTM_Wrapper, self).__init__()

    def fit(self, dataset: SMSDataset, **args):
        self._texts, self._targets = dataset.texts, dataset.targets
        self.word_dict = dataset.word_dict
        self._vocab_size = len(self.word_dict)
        n_hidden = args.get('n_hidden') or 5
        num_classes = args.get('num_classes') or 2
        embeddings_matrix = self._get_glove_embedding()
        self.model = BiLSTM_Attention(self._vocab_size, n_hidden,
                                      num_classes, embedding_dim=100, embedding_matrix=embeddings_matrix)

    def _get_glove_embedding(self, **args):
        FILE_PATH = args.get('file_path') or '../data/glove.6B.100d.txt'
        CHECKPOINT_PATH = args.get(
            'checkpoint_path') or '../checkpoints/glove100.npy'

        if not os.path.exists(FILE_PATH):
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

    def train(self, epochs, criterion, optimizer):
        np.save('../checkpoints/word_dict.npy', self.word_dict)
        global minist_loss
        self.criterion = criterion
        self.optimizer = optimizer
        loss_list = []
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            output, attention = self.model(self._texts)
            loss = criterion(output, self._targets)
            if ((epoch + 1) % 100 == 0) or ((loss < minist_loss) and epoch > 500):
                minist_loss = min(loss, minist_loss)
                print('Saving model in epoch: {0:d}'.format(epoch + 1))
                self.save_model(
                    '{0:s}/model_{1:03d}_{2:.3f}'.format(MODEL_FOLDER, epoch + 1, loss))
            if (epoch + 1) % 100 == 0:
                print('Epoch:', '%04d' % (epoch + 1),
                      'cost =', '{:.6f}'.format(loss))
            loss_list.append(loss)
            loss.backward()
            optimizer.step()
        return output, attention

    def predict(self, texts):
        original_texts = texts
        texts = torch.LongTensor(
            [np.asarray([self.word_dict[n] for n in text.split()]) for text in original_texts])

        # Predict
        predict, _ = self.model(texts)
        predicts = predict.data.max(1, keepdim=True)[1]
        for i, predict in enumerate(predicts):
            if predicts[i][0] == 0:
                print(original_texts[i], "is Bad Mean...")
            else:
                print(original_texts[i], "is Good Mean!!")

    def save_model(self, full_path: str):
        '''
        Argument:
            full_path {str} -- it's recommended to use formatted string to forms path
                            -- '{0:s}/model_{1:03d}_{2:.3f}'.format(MODEL_FOLDER, epoch+1, acc1)
        '''
        torch.save(self.model.state_dict(), full_path)

    def load_model(self, full_path: str, device='cpu'):
        self.model.load_state_dict(torch.load(
            full_path, map_location=device
        ))


if __name__ == "__main__":
    urandom.set_seed()
    # prepare
    dataset = SMSDataset()
    model_wrapper = BiLSTM_Wrapper()
    model_wrapper.fit(dataset)

    # train
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_wrapper.model.parameters(), lr=0.001)
    output, attention = model_wrapper.train(5000, criterion, optimizer)

    # show attention plot
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 5))  # [batch_size, n_step]
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(attention, cmap='viridis')
    ax.set_xticklabels([''] + ['first_word', 'second_word',
                               'third_word', 'forth_word'], fontdict={'fontsize': 14}, rotation=90)
    ax.set_yticklabels([''] + ['batch_1', 'batch_2', 'batch_3',
                               'batch_4', 'batch_5', 'batch_6'], fontdict={'fontsize': 14})
    plt.show()

    # predict
    test_texts = ['sorry hate you too', 'i love she much']
    model_wrapper.predict(test_texts)
