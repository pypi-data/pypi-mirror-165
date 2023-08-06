#!/usr/bin/env python3

from pyEdgeEval.common.multi_label.dataset_attributes import (
    CITYSCAPES_inst_labelIds,
    CITYSCAPES_labelIds,
    CITYSCAPES_label2trainId,
)

from .builder import DATASETS
from .custom_multilabel_dataset import (
    CustomMultiLabelDataset,
    OTFCustomMultiLabelDataset,
)

CITYSCAPES_CLASSES = (
    "road",
    "sidewalk",
    "building",
    "wall",
    "fence",
    "pole",
    "traffic light",
    "traffic sign",
    "vegetation",
    "terrain",
    "sky",
    "person",
    "rider",
    "car",
    "truck",
    "bus",
    "train",
    "motorcycle",
    "bicycle",
)
CITYSCAPES_PALETTE = [
    [128, 64, 128],
    [244, 35, 232],
    [70, 70, 70],
    [102, 102, 156],
    [190, 153, 153],
    [153, 153, 153],
    [250, 170, 30],
    [220, 220, 0],
    [107, 142, 35],
    [152, 251, 152],
    [70, 130, 180],
    [220, 20, 60],
    [255, 0, 0],
    [0, 0, 142],
    [0, 0, 70],
    [0, 60, 100],
    [0, 80, 100],
    [0, 0, 230],
    [119, 11, 32],
]
ignore_ids = [2, 3]


@DATASETS.register_module()
class CityscapesDataset(CustomMultiLabelDataset):
    CLASSES = CITYSCAPES_CLASSES
    PALETTE = CITYSCAPES_PALETTE

    def __init__(
        self,
        img_suffix="_leftImg8bit.png",
        edge_map_suffix="_gtProc_raw_edge.png",
        inst_sensitive=True,
        thin=False,
        **kwargs,
    ):

        if inst_sensitive:
            if thin:
                edge_map_suffix = "_gtProc_thin_isedge.png"
            else:
                edge_map_suffix = "_gtProc_raw_isedge.png"
        else:
            if thin:
                edge_map_suffix = "_gtProc_thin_edge.png"
            else:
                edge_map_suffix = "_gtProc_raw_edge.png"

        super(CityscapesDataset, self).__init__(
            img_suffix=img_suffix,
            edge_map_suffix=edge_map_suffix,
            inst_sensitive=inst_sensitive,
            **kwargs,
        )


@DATASETS.register_module()
class OTFCityscapesDataset(OTFCustomMultiLabelDataset):
    CLASSES = CITYSCAPES_CLASSES
    PALETTE = CITYSCAPES_PALETTE

    def __init__(
        self,
        img_suffix="_leftImg8bit.png",
        seg_map_suffix="_gtFine_labelIds.png",
        inst_map_suffix="_gtFine_instanceIds.png",
        labelIds=CITYSCAPES_labelIds,
        inst_labelIds=CITYSCAPES_inst_labelIds,
        ignore_indicies=[2, 3],
        label2trainId=CITYSCAPES_label2trainId,
        **kwargs,
    ):
        super(OTFCityscapesDataset, self).__init__(
            img_suffix=img_suffix,
            seg_map_suffix=seg_map_suffix,
            inst_map_suffix=inst_map_suffix,
            labelIds=labelIds,
            inst_labelIds=inst_labelIds,
            ignore_indices=ignore_indicies,
            label2trainId=label2trainId,
            **kwargs,
        )
