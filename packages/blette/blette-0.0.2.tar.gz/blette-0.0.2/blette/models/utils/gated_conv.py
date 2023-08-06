#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule, build_activation_layer, build_norm_layer


class GatedSpatialConv2d(ConvModule):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size=1,
        stride=1,
        padding=0,
        dilation=1,
        groups=1,
        bias=False,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=None,
        **kwargs,
    ):
        """Gated Spatial Conv2D
        :param in_channels:
        :param out_channels:
        :param kernel_size:
        :param stride:
        :param padding:
        :param dilation:
        :param groups:
        :param bias:
        """

        assert norm_cfg is not None
        assert act_cfg is not None

        super(GatedSpatialConv2d, self).__init__(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
            **kwargs,
        )

        self._gate_conv = nn.Sequential(
            build_norm_layer(norm_cfg, in_channels + 1)[-1],
            ConvModule(in_channels + 1, in_channels + 1, 1),
            build_activation_layer(act_cfg),
            ConvModule(in_channels + 1, 1, 1),
            build_norm_layer(norm_cfg, 1)[-1],
            nn.Sigmoid(),
        )

    def forward(self, input_features, gating_features):
        """forward
        :param input_features:
          - [NxCxHxW] featuers comming from the shape branch (canny branch).
        :param gating_features:
          - [Nx1xHxW] features comming from the texture branch (resnet)
             Only one channel feature map.
        :return:
        """
        alphas = self._gate_conv(
            torch.cat(
                [input_features, gating_features],
                dim=1,
            )
        )

        # residual connection
        input_features = input_features * (alphas + 1)

        return self.conv(input_features)
