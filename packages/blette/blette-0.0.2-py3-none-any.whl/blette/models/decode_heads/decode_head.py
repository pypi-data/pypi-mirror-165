#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

import torch
import torch.nn as nn
from mmcv.runner import BaseModule, auto_fp16, force_fp32
from mmseg.core import build_pixel_sampler
from mmseg.ops import resize

from ..builder import build_loss
from ..losses import accuracy, calc_metrics


class BaseDecodeHead(BaseModule, metaclass=ABCMeta):
    def __init__(
        self,
        in_channels,
        channels,
        *,
        num_classes,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
        in_index=-1,
        input_transform=None,
        loss_decode=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),  # TODO: update
        ignore_index=255,
        sampler=None,
        align_corners=False,
        init_cfg=dict(type="Normal", std=0.01),
    ):
        super(BaseDecodeHead, self).__init__(init_cfg)
        self._init_inputs(in_channels, in_index, input_transform)
        self.channels = channels
        self.num_classes = num_classes
        self.conv_cfg = conv_cfg
        self.norm_cfg = norm_cfg
        self.act_cfg = act_cfg
        self.in_index = in_index

        self.ignore_index = ignore_index
        self.align_corners = align_corners

        if isinstance(loss_decode, dict):
            self.loss_decode = build_loss(loss_decode)
        elif isinstance(loss_decode, (list, tuple)):
            self.loss_decode = nn.ModuleList()
            for loss in loss_decode:
                self.loss_decode.append(build_loss(loss))
        else:
            raise TypeError(
                f"loss_seg must be a dict or sequence of dict,\
                but got {type(loss_decode)}"
            )

        if sampler is not None:
            self.sampler = build_pixel_sampler(sampler, context=self)
        else:
            self.sampler = None

        self.fp16_enabled = False

    def extra_repr(self):
        """Extra repr."""
        s = (
            f"input_transform={self.input_transform}, "
            f"ignore_index={self.ignore_index}, "
            f"align_corners={self.align_corners}"
        )
        return s

    def _init_inputs(self, in_channels, in_index, input_transform):
        """Check and initialize input transforms.

        The in_channels, in_index and input_transform must match.
        Specifically, when input_transform is None, only single feature map
        will be selected. So in_channels and in_index must be of type int.
        When input_transform

        Args:
            in_channels (int|Sequence[int]): Input channels.
            in_index (int|Sequence[int]): Input feature index.
            input_transform (str|None): Transformation type of input features.
                Options: 'resize_concat', 'multiple_select', None.
                'resize_concat': Multiple feature maps will be resize to the
                    same size as first one and than concat together.
                    Usually used in FCN head of HRNet.
                'multiple_select': Multiple feature maps will be bundle into
                    a list and passed into decode head.
                None: Only one select feature map is allowed.
        """

        if input_transform is not None:
            assert input_transform in ["resize_concat", "multiple_select"]
        self.input_transform = input_transform
        self.in_index = in_index
        if input_transform is not None:
            assert isinstance(in_channels, (list, tuple))
            assert isinstance(in_index, (list, tuple))
            assert len(in_channels) == len(in_index)
            if input_transform == "resize_concat":
                self.in_channels = sum(in_channels)
            else:
                self.in_channels = in_channels
        else:
            assert isinstance(in_channels, int)
            assert isinstance(in_index, int)
            self.in_channels = in_channels

    def _transform_inputs(self, inputs):
        """Transform inputs for decoder.

        Args:
            inputs (list[Tensor]): List of multi-level img features.

        Returns:
            Tensor: The transformed inputs
        """

        if self.input_transform == "resize_concat":
            inputs = [inputs[i] for i in self.in_index]
            upsampled_inputs = [
                resize(
                    input=x,
                    size=inputs[0].shape[2:],
                    mode="bilinear",
                    align_corners=self.align_corners,
                )
                for x in inputs
            ]
            inputs = torch.cat(upsampled_inputs, dim=1)
        elif self.input_transform == "multiple_select":
            inputs = [inputs[i] for i in self.in_index]
        else:
            inputs = inputs[self.in_index]

        return inputs

    @auto_fp16()
    @abstractmethod
    def forward(self, inputs, **kwargs):
        """Placeholder of forward function."""
        pass

    def forward_train(
        self,
        inputs,
        img_metas,
        gt_semantic_edge,
        train_cfg,
    ):
        logits = self.forward(inputs=inputs, img_metas=img_metas)
        losses = self.losses(logits, gt_semantic_edge)
        return losses

    def forward_test(self, inputs, img_metas, test_cfg):
        """Forward function for testing."""
        return self.forward(inputs=inputs, img_metas=img_metas)

    @force_fp32(apply_to=("logit",))
    def losses(self, logit, label):
        """Compute edge loss."""
        loss = dict()

        logit = resize(
            input=logit,
            size=label.shape[2:],  # (b, cls, h, w)
            mode="bilinear",
            align_corners=self.align_corners,
        )

        if not isinstance(self.loss_decode, nn.ModuleList):
            losses_edge = [self.loss_decode]
        else:
            losses_edge = self.loss_decode
        for loss_edge in losses_edge:
            if loss_edge.loss_name not in loss:
                loss[loss_edge.loss_name] = loss_edge(
                    edge=logit,
                    edge_label=label,
                    ignore_index=self.ignore_index,
                )
            else:
                loss[loss_edge.loss_name] += loss_edge(
                    edge=logit,
                    edge_label=label,
                    ignore_index=self.ignore_index,
                )

        # for binary
        if label.size(1) == 1:
            # FIXME: awfully high... might be only positives (doesn't include false positive)
            label = label.squeeze(1)
            loss["acc_edge"] = accuracy(logit, label)

        for name, v in calc_metrics(logit, label).items():
            loss[name] = v

        return loss
