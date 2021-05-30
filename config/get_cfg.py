from detectron2.config import CfgNode
from .defaults import _C


def get_cfg() -> CfgNode:
    """
    Get a copy of the default config.

    Returns:
        a detectron2 CfgNode instance.
    """

    return _C.clone()
