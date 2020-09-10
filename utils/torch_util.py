import random
import numpy as np
import torch
import matplotlib.pyplot as plt
from torchvision.utils import make_grid


GLOBAL_SEED = 1


def set_seed(seed=GLOBAL_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def worker_init_fn(worker_id):
    '''
    For dataloader
    '''
    set_seed(GLOBAL_SEED + worker_id)


def accuracy_calc(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, largest=True, sorted=True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def adjust_learning_rate(optimizer, epoch, original_lr, decay_step):
    """Sets the learning rate to the initial LR decayed by 10 every step
    """
    lr = original_lr * (0.1 ** (epoch // decay_step))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


# tring to un normalize the image so that a normal image can be displayed, however failed
def unnormalization(normalization, img_batch):
    mean, std = normalization
    unnor_img_batch = img_batch
    for i, channel in enumerate(unnor_img_batch):
        channel = channel * std[i] + mean[i]
    unnor_img_batch = unnor_img_batch.mul(255)
    return unnor_img_batch
