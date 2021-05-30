import multiprocessing as mp
import cv2
import numpy as np

from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from .predictor import VisualizationDemo
from config.get_cfg import get_cfg

from tqdm.auto import tqdm, trange
from tqdm import tqdm_notebook


def decode_recognition(rec):
    CTLABELS = [
        ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-',
        '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
        '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
        'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e',
        'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
        't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'
    ]

    s = ''
    for c in rec:
        c = int(c)
        if c < 95:
            s += CTLABELS[c]
        elif c == 95:
            s += u'口'
    return s


def predict(img, device="cpu"):
    cfg = get_cfg()
    cfg.merge_from_file("./checkpoints/batext/attn_R_50.yaml")
    cfg.merge_from_list(["MODEL.WEIGHTS", "./checkpoints/batext/tt_attn_R_50.pth"])
    cfg.merge_from_list(["MODEL.DEVICE", device])

    confidence = 0.5
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = confidence
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = confidence
    cfg.MODEL.FCOS.INFERENCE_TH_TEST = confidence
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = confidence
    cfg.freeze()

    demo = VisualizationDemo(cfg)
    if isinstance(img, str):
        img = cv2.imread(img) # img_path
    elif hasattr(img, 'shape'): # cv2 format
        pass
    else: # PIL format
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    predictions, visualized_output = demo.run_on_image(img)
    words = [decode_recognition(p) for p in predictions["instances"].recs]
    visualized_img = visualized_output.get_image()

    return visualized_img, words
