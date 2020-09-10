"""
@Author: peviroy
@Date: 2020-09-09
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 17:00
"""
import os
import time
import torch
import numpy as np

from utils.preprocessing import TextPurifier
from utils.Meter import AverageMeter, ProgressMeter
from .BiLSTM import BiLSTM_Attention
from utils import accuracy_calc
from dataset import SMSTransform


class BiLSTM_Wrapper:
    '''
    A union for a series of operations of BiLSTM. e.g. data transform, train, predict...
    '''

    def __init__(self, device, word_dict):
        '''
        Empty wrapper created, use 'fit and train' to start train a new model or use 'load' to get a pretrained model
        '''
        super(BiLSTM_Wrapper, self).__init__()
        self.device = device
        self.word_dict = word_dict

    def fit(self, **args):
        self._vocab_size = len(self.word_dict)
        n_hidden = args.get('n_hidden') or 5
        num_classes = args.get('num_classes') or 2
        embeddings_matrix = self._get_glove_embedding()
        self.model = BiLSTM_Attention(self._vocab_size, n_hidden,
                                      num_classes, embedding_dim=100, embedding_matrix=embeddings_matrix, device=self.device)
        self.model = self.model.to(self.device)

    def _get_glove_embedding(self, **args):
        FILE_PATH = args.get('file_path') or 'data/glove.6B.100d.txt'
        CHECKPOINT_PATH = args.get(
            'checkpoint_path') or 'checkpoints/glove100.npy'

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

    def train(self, trainloader, criterion, optimizer, current_epoch=0):
        batch_time = AverageMeter(name='Time', fmt=':6.3f')
        losses = AverageMeter('Loss', ':.4e')
        top1_acc = AverageMeter('Acc@1', ':6.2f')  # top 1 accuracy
        progress = ProgressMeter(   # log
            len(trainloader),
            [batch_time, losses, top1_acc],
            prefix="[Train] Epoch: [{}]".format(current_epoch + 1))

        # train mode
        self.model.train()

        end = time.time()
        for batch_cnt, batch_data in enumerate(trainloader):
            # move into specific device
            text_batch, label_batch = batch_data
            text_batch, label_batch = text_batch.to(
                self.device), label_batch.to(self.device)

            # output
            outputs, attention = self.model(text_batch)

            # calculate loss
            loss = criterion(outputs, label_batch)

            # measure accuracy and record loss
            acc1 = accuracy_calc(outputs, label_batch, topk=[1])

            # detach makes no grad,
            losses.update(loss.detach().item(), n=text_batch.size(0))
            top1_acc.update(acc1[0].item(), n=text_batch.size(0))

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            # display
            progress.display(batch_cnt + 1)
        return losses.avg, top1_acc.avg, progress.get(batch_cnt + 1)

    def test(self, testloader, current_epoch=0):
        print('In Test:')
        # time spent in a batch
        batch_time = AverageMeter(name='Time', fmt=':6.3f')
        top1_acc = AverageMeter('Acc@1', ':6.2f')  # top 1 accuracy
        progress = ProgressMeter(   # log
            len(testloader),
            [batch_time, top1_acc],
            prefix="[Test] Epoch: [{}]".format(current_epoch + 1))

        self.model.eval()
        with torch.no_grad():
            end = time.time()
            for batch_cnt, batch_data in enumerate(testloader):
                text_batch, label_batch = batch_data
                text_batch, label_batch = text_batch.to(
                    self.device), label_batch.to(self.device)

                outputs, attention = self.model(text_batch)

                # measure accuracy and record loss
                acc1 = accuracy_calc(outputs, label_batch, topk=[1])
                top1_acc.update(acc1[0].item(), text_batch.size(0))

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

                # display
                progress.display(batch_cnt + 1)

        return top1_acc.avg, progress.get(batch_cnt + 1)

    def predict(self, texts):
        original_texts = texts
        texts = TextPurifier(texts).purify()
        print(texts)

        transform = SMSTransform()
        new_texts, _, _ = transform(texts)
        # new_texts = []
        # for text in texts:
        #     new_texts.append(torch.LongTensor(np.asarray(
        #         [self.word_dict[n] for n in text.split()])))

        with torch.no_grad():
            new_texts = new_texts.to(self.device)
            predict, attention = self.model(new_texts)
            predicts = predict.data.max(1, keepdim=True)[1]
            for i, predict in enumerate(predicts):
                if predicts[i][0] == 0:
                    print(original_texts[i], "is Ham email")
                else:
                    print(original_texts[i], "is Spam email")
        pic_save_path = '.'
        self.draw_attention(attention, pic_save_path)
        return predicts[0][0], pic_save_path    # support one text predict only

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

    def draw_attention(self, attention, save_path='.'):
        # show attention plot
        import matplotlib.pyplot as plt
        fig = plt.figure()  # [batch_size, n_step]
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(attention, cmap='viridis')
        # ax.set_xticklabels([''] + ['first_word', 'second_word',
        #    'third_word', 'forth_word'], fontdict={'fontsize': 14}, rotation=90)
        # ax.set_yticklabels([''] + ['batch_1', 'batch_2', 'batch_3',
        #    'batch_4', 'batch_5', 'batch_6'], fontdict={'fontsize': 14})
        plt.savefig(save_path)

        plt.show()
