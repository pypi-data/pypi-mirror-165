#!/usr/bin/env python3

import torch
import torch.nn as nn

from ..builder import LOSSES

# from .cross_entropy_loss import cross_entropy


@LOSSES.register_module()
class StableMultiLabelEdgeLoss(nn.Module):
    def __init__(
        self,
        loss_weight=1.0,
        loss_name="loss_stable_multilabel_edge",
        # reduction="mean",
        # avg_non_ignore=False,
    ):
        super().__init__()
        self.loss_weight = loss_weight
        self._loss_name = loss_name

        # self.reduction = reduction
        # self.avg_non_ignore = avg_non_ignore
        # self.cls_criterion = cross_entropy

    # def forward(
    #     self,
    #     edge,
    #     edge_label,
    #     weight=None,
    #     avg_factor=None,
    #     reduction_override=None,
    #     ignore_index=-100,
    #     avg_non_ignore=False,
    #     **kwargs,
    # ):
    #     assert reduction_override in (None, "none", "mean", "sum")
    #     reduction = reduction_override if reduction_override else self.reduction
    #     # Note: for BCE loss, label < 0 is invalid.
    #     loss_cls = self.loss_weight * self.cls_criterion(
    #         edge,
    #         edge_label,
    #         weight,
    #         class_weight=None,
    #         reduction=reduction,
    #         avg_factor=avg_factor,
    #         avg_non_ignore=self.avg_non_ignore,
    #         ignore_index=ignore_index,
    #         **kwargs,
    #     )
    #     return loss_cls

    def forward(
        self,
        edge,  # logits
        edge_label,
        weight=None,
        ignore_index=255,
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
            # compute a pos_weight for each image
            pos_weight = (num_neg / num_pos).clamp(min=1, max=num_total)

            max_val = (-pred).clamp_min_(0)
            log_weight = 1 + (pos_weight - 1) * target
            loss = (
                pred
                - pred * target
                + log_weight
                * (
                    max_val
                    + torch.log(torch.exp(-max_val) + torch.exp(-pred - max_val))
                )
            )

            loss = loss.mean()
            loss_total = loss_total + loss

        loss_total = loss_total / edge_label.size(0)
        return self.loss_weight * loss_total

    @property
    def loss_name(self):
        return self._loss_name
