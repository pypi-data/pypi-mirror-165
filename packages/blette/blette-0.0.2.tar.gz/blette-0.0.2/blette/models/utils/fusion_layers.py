#!/usr/bin/env python3

import torch.nn as nn

from mmcv.cnn import ConvModule


class LocationAdaptiveLearner(nn.Module):
    """docstring for LocationAdaptiveLearner"""

    def __init__(
        self,
        in_channels,
        out_channels,
        conv_cfg,
        norm_cfg,
        act_cfg,
    ):
        super(LocationAdaptiveLearner, self).__init__()

        self.conv1 = ConvModule(
            in_channels,
            out_channels,
            1,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
        )
        self.conv2 = ConvModule(
            out_channels,
            out_channels,
            1,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
        )
        self.conv3 = ConvModule(
            out_channels,
            out_channels,
            1,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=None,
        )

    def forward(self, x):
        # x:side5_w (N, 19*4, H, W)
        num_backbone = 4
        num_classes = x.shape[1] // num_backbone
        x = self.conv1(x)  # (N, 19*4, H, W)
        x = self.conv2(x)  # (N, 19*4, H, W)
        x = self.conv3(x)  # (N, 19*4, H, W)
        x = x.view(
            x.size(0), num_classes, num_backbone, x.size(2), x.size(3)
        )  # (N, 19, 4, H, W)
        return x
