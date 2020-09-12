"""
@Author: peviroy
@Date: 2020-09-08
@Last Modified by: peviroy
@Last Modified time: 2020-09-10 23:40
"""

# make sure to change to the projict directory
import warnings
from utils import adjust_learning_rate
from dataset import SMSDataset, SMSTransform, SMSDataset_generator
from utils import draw_acc_loss
from model.BiLSTM_Wrapper import BiLSTM_Wrapper
from model.LSTM_Wrapper import LSTM_Wrapper
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
import torch.nn as nn
import torch
import argparse
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])


parser = argparse.ArgumentParser(description="Main entry for BiLSTM")
parser.add_argument('--model-folder', default='./checkpoints',
                    help='folder to save models', dest='model_folder')
parser.add_argument('--resume', default='', type=str,
                    help='path to latest checkpoint')
parser.add_argument('--pre-epoch', default=0, type=int,
                    help='previous epoch (default: none)', dest='pre_epoch')
parser.add_argument('--data', default='./data/spam.csv',
                    help='where the data set is stored')
parser.add_argument('--batch', default=256, type=int,
                    help='batch size of data input(default: 64)')
parser.add_argument('--epoch', default=2000, type=int,
                    help='the number of cycles to train the model(default: 200)')
parser.add_argument('--save', default='./checkpoints/model_ham/',
                    help='dir for saving document file')
parser.add_argument('--lr', default='0.001', type=float,
                    help='learning rate(default: 0.001)')
parser.add_argument('--lr-decay-step', default='600', type=int,
                    help='lr decayed by 10 every step', dest='lr_decay_step')
parser.add_argument('--weight-decay', default=5e-4, type=float,
                    help='weight decay (default: 5e-4)', dest='weight_decay')
parser.add_argument('--gpu', default=0, type=int, help='GPU id to use')
parser.add_argument('--validate', default=False,
                    type=bool, help='validation mode')
parser.add_argument('--test', default=False, type=bool, help='test only mode')
parser.add_argument('--predict', default=False,
                    type=bool, help='predict only mode')
parser.add_argument('--model', default='attention', type=str,
                    help='generator')
parser.add_argument('--sequence-length', default=5, type=int,
                    help='sequence_length for generator model')
parser.add_argument('-seed', default=417241, type=int,
                    help='seed used for the random permutation.')
args = parser.parse_args()

best_acc1 = 0  # global
seed = args.seed


def main():
    """There we perform pre-processing work, for example, setting up GPU, prepare directory.
    """
    args = parser.parse_args()

    # Solve path problem
    if not os.path.exists(args.data):
        warnings.warn('No such dataset:')
        raise Exception("Invalid dataset path:", args.data)
    if not os.path.exists(args.model_folder):
        os.makedirs(args.model_folder)
    if not os.path.exists(args.save):
        os.makedirs(args.save)

    # Only support single gpu training right now
    if not torch.cuda.is_available() or args.gpu == -1:
        warnings.warn('No GPU is not found. Use CPU')
        device = torch.device('cpu')
    else:
        print('Using gpu: {0} in device: {1}'.format(
            args.gpu, torch.cuda.get_device_name()))
        device = torch.device('cuda', args.gpu)
    main_worker(device, args)


def main_worker(device, args):
    global best_acc1  # global

    # *Hpyer argument
    EPOCH = args.epoch
    PRE_EPOCH = args.pre_epoch
    BATCH_SIZE = args.batch
    LR = args.lr            # learning rate
    WEIGHT_DECAY = args.weight_decay

    # *Data loading
    transform = SMSTransform(args.save)

    if args.model == 'generator':
        sms_dataset = SMSDataset_generator(
            args.sequence_length, cate_type='ham', transform=transform, file_path=args.data)
        train_dataloader = DataLoader(sms_dataset,
                                      batch_size=BATCH_SIZE)

        model_wrapper = LSTM_Wrapper(
            device=device, word_dict=sms_dataset.word_dict, index_dict=sms_dataset.index_dict, pre_file_path=args.save)
        model_wrapper.fit()

        # resume frome a checkpoint
        if args.resume:
            if os.path.isfile(args.resume):
                print('loading pretrained model: {0:s}'.format(args.resume))
                model_wrapper.load_model(full_path=args.resume, device=device)
            else:
                warnings.warn('No such checkpoint: {0:s}'.format(args.resume))

        criterion = nn.CrossEntropyLoss().to(device)
        optimizer = optim.Adam(model_wrapper.model.parameters(), lr=LR,
                               weight_decay=WEIGHT_DECAY)

        if args.predict:
            print(model_wrapper.predict(
                ['Even my brother is not like to'], 50))
            return

        loss_list = []
        for epoch in range(PRE_EPOCH, EPOCH):
            print('In Train:')
            state_h, state_c = model_wrapper.model.init_state(
                args.sequence_length)

            train_loss, train_logger = model_wrapper.train(
                train_dataloader, criterion, optimizer, state_h, state_c, current_epoch=epoch)
            loss_list.append(train_loss)
            # remember best acc@1 and save checkpoint
            if ((epoch + 1) % 100 == 0):
                print('Saving model in epoch: {0:d}'.format(epoch + 1))
                model_wrapper.save_model(
                    full_path='{0:s}/model_s_{1:03d}_{2:.3f}'.format(args.save, epoch + 1, train_loss))

        print(model_wrapper.predict(['Even my brother is not like to'], 50))

        draw_acc_loss(PRE_EPOCH, EPOCH, train_acc=None,
                      train_loss=loss_list, test_acc=None, savedir=args.save)

        print('Saving Final model in epoch')
        model_wrapper.save_model(
            full_path='{0:s}/model_s_final'.format(args.save))
        print("Training Finish")
        return

    sms_dataset = SMSDataset(transform=transform,
                             file_path=args.data)

    train_size = int(0.8 * len(sms_dataset))
    test_size = len(sms_dataset) - train_size
    train_dataset, test_dataset = random_split(
        sms_dataset, [train_size, test_size],
        generator=torch.Generator().manual_seed(seed))

    # train_dataset = SMSDataset(train_dataset)
    # test_dataset = SMSDataset(test_dataset)

    train_dataloader = DataLoader(train_dataset,
                                  batch_size=BATCH_SIZE,
                                  shuffle=True,
                                  num_workers=4)

    test_dataloader = DataLoader(test_dataset,
                                 batch_size=BATCH_SIZE,
                                 shuffle=False,
                                 num_workers=4)

    # *create model
    model_wrapper = BiLSTM_Wrapper(
        device=device, word_dict=sms_dataset.word_dict, pre_file_path=args.save)
    model_wrapper.fit()

    # resume frome a checkpoint
    if args.resume:
        if os.path.isfile(args.resume):
            print('loading pretrained model: {0:s}'.format(args.resume))
            model_wrapper.load_model(full_path=args.resume, device=device)
        else:
            warnings.warn('No such checkpoint: {0:s}'.format(args.resume))

    # *loss function and optimizer
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model_wrapper.model.parameters(), lr=LR,
                           weight_decay=WEIGHT_DECAY)

    if args.predict:
        model_wrapper.predict(texts=[
            'Even my brother is not like to speak with me. They treat me like aids patent.',
            'SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575. Cost 150p/day, 6days, 16+ TsandCs apply Reply HL 4 info'])

    # *Start traning or testing
    # test mode: get the accuracy of the model on test dataset
    if args.test:
        print('Test mode')
        model_wrapper.test(
            test_dataloader, current_epoch=0)

        return

    # if not to validate it, train it
    with open(args.save + '/accuracy.txt', 'w') as acc_f:
        with open(args.save + '/log.txt', 'w') as log_f:
            # record info in every epoch
            loss_list = []
            train_accuracy_list = []
            test_accuracy_list = []
            for epoch in range(PRE_EPOCH, EPOCH):
                print('In Train:')
                adjust_learning_rate(
                    optimizer, epoch, original_lr=args.lr, decay_step=args.lr_decay_step)
                # the task of outputing grogress has been completed within the train and test function
                train_loss, train_acc1, train_logger = model_wrapper.train(
                    train_dataloader, criterion, optimizer)

                acc1, test_logger = model_wrapper.test(
                    test_dataloader, current_epoch=epoch)
                # remember best acc@1 and save checkpoint
                if ((acc1 > best_acc1) and epoch > 500) | ((epoch + 1) % 100 == 0):
                    best_acc1 = max(acc1, best_acc1)
                    print('Saving model in epoch: {0:d}'.format(epoch + 1))
                    model_wrapper.save_model(
                        full_path='{0:s}/model_{1:03d}_{2:.3f}'.format(args.save, epoch + 1, acc1))

                loss_list.append(train_loss)
                train_accuracy_list.append(train_acc1)
                test_accuracy_list.append(acc1)

                # # log
                log_f.write(train_logger)
                log_f.write('\n')
                log_f.flush()
                acc_f.write(test_logger)
                acc_f.write('\n')
                acc_f.flush()

    # Epoch finished.
    draw_acc_loss(PRE_EPOCH, EPOCH, train_acc=train_accuracy_list,
                  train_loss=loss_list, test_acc=test_accuracy_list, savedir=args.save)

    print('Saving Final model in epoch')
    model_wrapper.save_model(
        full_path='{0:s}/model_final'.format(args.save))
    print("Training Finish")


if __name__ == '__main__':
    main()
