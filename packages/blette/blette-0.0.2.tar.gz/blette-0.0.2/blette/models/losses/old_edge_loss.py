#!/usr/bin/env python3

"""Old losses that is converted for mmsegmentation

FIXME: update the losses so that we can reuse them
"""

import torch
import torch.nn as nn

from ..builder import LOSSES


@LOSSES.register_module()
class MultiLabelEdgeLoss(nn.Module):
    def __init__(
        self,
        loss_weight=1.0,
        loss_name="loss_multilabel_edge",
    ):
        super().__init__()
        self.loss_weight = loss_weight
        self._loss_name = loss_name

    def forward(
        self,
        edge,  # logits
        edge_label,
        weight=None,
        **kwargs,
    ):
        loss_total = 0

        # FIXME: could optimize for batched loss
        for i in range(edge_label.size(0)):  # iterate for batch size
            pred = edge[i]
            target = edge_label[i]

            num_pos = torch.sum(target)  # true positive number
            num_total = target.size(-1) * target.size(-2)  # true total number
            num_neg = num_total - num_pos
            pos_weight = (num_neg / num_pos).clamp(
                min=1, max=num_total
            )  # compute a pos_weight for each image

            max_val = (-pred).clamp(min=0)
            log_weight = 1 + (pos_weight - 1) * target
            loss = (
                pred
                - pred * target
                + log_weight
                * (max_val + ((-max_val).exp() + (-pred - max_val).exp()).log())
            )

            loss = loss.mean()
            loss_total = loss_total + loss

        loss_total = loss_total / edge_label.size(0)
        return self.loss_weight * loss_total

    @property
    def loss_name(self):
        return self._loss_name
