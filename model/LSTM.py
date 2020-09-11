"""
@Author: peviroy
@Date: 2020-09-10
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 21:40
"""

import torch
from torch import nn


class LSTM_Generator(nn.Module):
    def __init__(self, device, vocab_size, n_hidden, embedding_dim, embedding_matrix=None):
        super(LSTM_Generator, self).__init__()
        self.n_hidden = 128
        self.num_layers = 3
        self.device = device

        if embedding_matrix is None:
            self.embedding = nn.Embedding(vocab_size, embedding_dim)
        else:  # pretrained
            self.embedding = nn.Embedding.from_pretrained(
                torch.FloatTensor(embedding_matrix), freeze=True)

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=self.n_hidden,
            num_layers=self.num_layers,
            dropout=0.2,
        )
        self.fc = nn.Linear(self.n_hidden, vocab_size)

    def forward(self, X, prev_state):
        input = self.embedding(X)
        output, state = self.lstm(input, prev_state)
        logits = self.fc(output)

        return logits, state

    def init_state(self, sequence_length):
        return (torch.zeros(self.num_layers, sequence_length, self.n_hidden),
                torch.zeros(self.num_layers, sequence_length, self.n_hidden))
