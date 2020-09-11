"""
@Author: Hwan Jung(Jeff Jung) @graykode
@Date: 2020-08-14
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 16:30
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class BiLSTM_Attention(nn.Module):
    def __init__(self, vocab_size, n_hidden, num_classes, embedding_dim, device=None, embedding_matrix=None):
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
        self.device = device

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
        return context, soft_attn_weights.data

    def forward(self, X):
        # input : [batch_size, len_seq, embedding_dim]
        input = self.embedding(X)
        # input : [len_seq, batch_size, embedding_dim]
        input = input.permute(1, 0, 2)

        # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        hidden_state = torch.zeros(
            1 * 2, len(X), self.n_hidden).to(self.device)
        # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        cell_state = torch.zeros(1 * 2, len(X), self.n_hidden).to(self.device)

        # output : [len_seq, batch_size, n_hidden]
        output, (final_hidden_state, final_cell_state) = self.lstm(
            input, (hidden_state, cell_state))
        # output : [batch_size, len_seq, n_hidden]
        output = output.permute(1, 0, 2)
        attn_output, attention = self.attention_net(output, final_hidden_state)
        # self.out(.) : [batch_size, num_classes], attention : [batch_size, n_step]
        return self.out(attn_output), attention
