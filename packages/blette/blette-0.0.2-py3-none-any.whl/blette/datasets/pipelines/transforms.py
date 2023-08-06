#!/usr/bin/env python3

"""Extend and add tranformations.

Skipped:
- RandomCutOut
- RandomMosaic
"""

import numpy as np

import mmcv
from mmseg.datasets.pipelines.transforms import (
    Resize as MMSEG_Resize,
    Pad as MMSEG_Pad,
    RandomRotate as MMSEG_RandomRotate,
)

from ..builder import PIPELINES


@PIPELINES.register_module(force=True)
class Resize(MMSEG_Resize):

    _supported_types = ("gt_semantic_seg", "gt_semantic_edge", "gt_inst_seg")

    def _resize_seg(self, results):
        for key in results.get("seg_fields", []):

            assert (
                key in self._supported_types
            ), f"ERR: {key} is not in {self._supported_types}"

            """Semantic edge:
            - should work fine for most cases
            - however, the edges might be thicker than how it was preprocessed
            """

            """Instance segmentation:
            - formatting matters for cv2 input
            - https://stackoverflow.com/questions/15245262/opencv-mat-element-types-and-their-sizes
            - 32-bit signed integer should work (CV_32S)
            """

            if self.keep_ratio:
                gt_seg = mmcv.imrescale(
                    results[key], results["scale"], interpolation="nearest"
                )
            else:
                gt_seg = mmcv.imresize(
                    results[key], results["scale"], interpolation="nearest"
                )
            results[key] = gt_seg


@PIPELINES.register_module(force=True)
class Pad(MMSEG_Pad):
    def __init__(
        self,
        size=None,
        size_divisor=None,
        pad_val=0,
        seg_pad_val=255,  # NOTE: 255 == background / ignore
        edge_pad_val=0,  # NOTE: 0 == background
        inst_pad_val=0,  # NOTE: 0 == background
    ):
        super().__init__(
            size=size,
            size_divisor=size_divisor,
            pad_val=pad_val,
            seg_pad_val=seg_pad_val,
        )
        self.edge_pad_val = edge_pad_val
        self.inst_pad_val = inst_pad_val

    def _pad_seg(self, results):
        for key in results.get("seg_fields", []):
            if key == "gt_semantic_edge":
                results[key] = mmcv.impad(
                    results[key],
                    shape=results["pad_shape"][:2],
                    pad_val=self.edge_pad_val,
                )
            elif key == "gt_inst_seg":
                results[key] = mmcv.impad(
                    results[key],
                    shape=results["pad_shape"][:2],
                    pad_val=self.inst_pad_val,
                )
            elif key == "gt_semantic_seg":
                results[key] = mmcv.impad(
                    results[key],
                    shape=results["pad_shape"][:2],
                    pad_val=self.seg_pad_val,
                )
            else:
                raise ValueError(f"{key} is not supported")


@PIPELINES.register_module(force=True)
class RandomRotate(MMSEG_RandomRotate):
    def __init__(
        self,
        prob,
        degree,
        pad_val=0,
        seg_pad_val=255,  # NOTE: 255 == background / ignore
        center=None,
        auto_bound=False,
        edge_pad_val=0,  # NOTE: 0 == background
        inst_pad_val=0,  # NOTE: 0 == background
    ):
        super().__init__(
            prob=prob,
            degree=degree,
            pad_val=pad_val,
            seg_pad_val=seg_pad_val,
            center=center,
            auto_bound=auto_bound,
        )
        self.edge_pad_val = (edge_pad_val,)
        self.inst_pad_val = inst_pad_val

    def __call__(self, results):
        rotate = True if np.random.rand() < self.prob else False
        degree = np.random.uniform(min(*self.degree), max(*self.degree))
        if rotate:
            # rotate image
            results["img"] = mmcv.imrotate(
                results["img"],
                angle=degree,
                border_value=self.pal_val,
                center=self.center,
                auto_bound=self.auto_bound,
            )

            # rotate segs
            for key in results.get("seg_fields", []):
                if key == "gt_semantic_edge":
                    results[key] = mmcv.imrotate(
                        results[key],
                        angle=degree,
                        pad_val=0,
                        center=self.center,
                        auto_bound=self.auto_bound,
                        interpolation="nearest",
                    )
                elif key == "gt_inst_seg":
                    results[key] = mmcv.imrotate(
                        results[key],
                        angle=degree,
                        pad_val=self.inst_pad_val,
                        center=self.center,
                        auto_bound=self.auto_bound,
                        interpolation="nearest",
                    )
                elif key == "gt_semantic_seg":
                    results[key] = mmcv.imrotate(
                        results[key],
                        angle=degree,
                        border_value=self.seg_pad_val,
                        center=self.center,
                        auto_bound=self.auto_bound,
                        interpolation="nearest",
                    )
                else:
                    raise ValueError(f"ERR: {key} is not supported")
        return results
