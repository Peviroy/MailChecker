import random
import numpy as np
import torch
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
