#!/usr/bin/env python3

import numpy as np

from mmcv.parallel import DataContainer as DC
from mmseg.datasets.pipelines.formatting import (
    ToDataContainer as MMSEG_ToDataContainer,
    to_tensor,
)

from ..builder import PIPELINES


@PIPELINES.register_module(force=True)
class ToDataContainer(MMSEG_ToDataContainer):
    def __init__(
        self,
        fields=(
            dict(key="img", stack=True),
            dict(key="gt_semantic_seg"),
            dict(key="gt_semantic_edge"),
        ),
    ):
        self.fields = fields


@PIPELINES.register_module()
class FormatImage(object):
    def __call__(self, results):
        # input image
        if "img" in results:
            img = results["img"]
            if len(img.shape) < 3:
                img = np.expand_dims(img, -1)
            img = np.ascontiguousarray(img.transpose(2, 0, 1))
            results["img"] = DC(to_tensor(img), stack=True)

        return results

    def __repr__(self):
        return self.__class__.__name__


@PIPELINES.register_module()
class FormatEdge(object):
    def __call__(self, results):
        # non-otf
        if "gt_semantic_edge" in results:
            edge = results["gt_semantic_edge"]

            if results.get("binary", None):
                # No need for hacks to convert dataset
                results["gt_semantic_edge"] = DC(
                    to_tensor(edge[None, ...].astype(np.int64)),
                    stack=True,
                )
            else:
                # HACK: decode RGB to 24bit array
                # it's only possible to encode 24 classes
                edge = np.unpackbits(
                    edge,
                    axis=2,
                )[:, :, -1 : -(results["num_classes"] + 1) : -1]
                edge = np.ascontiguousarray(edge.transpose(2, 0, 1))

                # convert to long
                results["gt_semantic_edge"] = DC(
                    to_tensor(edge.astype(np.int64)),
                    stack=True,
                )
        elif "gt_semantic_seg" in results:
            mask2edge = results.get("mask2edge", None)
            assert mask2edge, "ERR: no mask2edge inside `results`"

            if results["inst_sensitive"]:
                inst_map = results.get("gt_inst_seg", None)
                assert inst_map is not None, "ERR: instance map is not available"
                out = mask2edge(
                    mask=results["gt_semantic_seg"],
                    inst_mask=inst_map,
                )
                # remove it from memory?
                del results["gt_inst_seg"]
            else:
                out = mask2edge(mask=results["gt_semantic_seg"])

            results["gt_semantic_edge"] = DC(
                to_tensor(out["edge"].astype(np.int64)),
                stack=True,
            )

        return results


# avoid naming `DefaultFormatBundle` since we want to use the original
@PIPELINES.register_module(force=True)
class EdgeFormatBundle(object):
    def __init__(self):
        self.format_image = FormatImage()
        self.format_edge = FormatEdge()

    def __call__(self, results):
        # chain together formatting
        results = self.format_image(results)
        results = self.format_edge(results)
        return results

    def __repr__(self):
        return self.__class__.__name__
