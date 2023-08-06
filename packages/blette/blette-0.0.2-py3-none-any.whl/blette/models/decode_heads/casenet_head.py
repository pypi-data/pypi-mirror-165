#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule
from mmcv.runner import force_fp32
from mmseg.ops import resize

from ..builder import HEADS
from ..losses import calc_metrics
from .decode_head import BaseDecodeHead


@HEADS.register_module()
class CASENetHead(BaseDecodeHead):
    def __init__(
        self,
        **kwargs,
    ):
        super(CASENetHead, self).__init__(
            input_transform="multiple_select",
            **kwargs,
        )

        """
        NOTES:
        - make sure to not add activations (especially before output)
        - in the paper, they did not add batch normalization
        """

        self.side1 = ConvModule(
            in_channels=self.in_channels[0],
            out_channels=1,
            kernel_size=1,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side2 = ConvModule(
            in_channels=self.in_channels[1],
            out_channels=1,
            kernel_size=1,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side3 = ConvModule(
            in_channels=self.in_channels[2],
            out_channels=1,
            kernel_size=1,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side4 = ConvModule(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            kernel_size=1,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.fuse = ConvModule(
            in_channels=self.num_classes * 4,
            out_channels=self.num_classes,
            kernel_size=1,
            bias=True,
            groups=self.num_classes,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )

    def forward(self, inputs, img_metas):

        img_shape = img_metas[0]["img_shape"][:2]  # input size of network

        x = [i for i in inputs]
        # x = self._transform_inputs(inputs)

        s1 = resize(  # (B, 1, H, W)
            self.side1(x[0]),
            size=img_shape,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s2 = resize(  # (B, 1, H, W)
            self.side2(x[1]),
            size=img_shape,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s3 = resize(  # (B, 1, H, W)
            self.side3(x[2]),
            size=img_shape,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s4 = resize(  # (B, 19, H, W)
            self.side4(x[4]),
            size=img_shape,
            mode="bilinear",
            align_corners=self.align_corners,
        )

        slice4 = s4[:, 0:1, :, :]
        fuse = torch.cat((slice4, s1, s2, s3), 1)
        for i in range(s4.size(1) - 1):
            slice4 = s4[:, i + 1 : i + 2, :, :]
            fuse = torch.cat((fuse, slice4, s1, s2, s3), 1)

        fuse = self.fuse(fuse)

        return dict(
            fuse=fuse,
            side5=s4,
        )

    def forward_test(self, inputs, img_metas, test_cfg):
        """use test_cfg's edge_key to choose which output"""
        edge_key = test_cfg.get("edge_key", "fuse")
        return self.forward(inputs, img_metas)[edge_key]

    @force_fp32(apply_to=("logit",))
    def losses(self, logit, label):
        """Need to supervise all output logits"""
        assert isinstance(logit, dict), f"logit should be a dict but got {type(logit)}"

        loss = dict()

        for k, pred in logit.items():
            pred = resize(
                input=pred,
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
                    loss[k + "_" + loss_edge.loss_name] = loss_edge(
                        edge=pred,
                        edge_label=label,
                        ignore_index=self.ignore_index,
                    )
                else:
                    loss[k + "_" + loss_edge.loss_name] += loss_edge(
                        edge=pred,
                        edge_label=label,
                        ignore_index=self.ignore_index,
                    )

            if k == "fuse":
                # calculate metrics for 'fuse'
                for name, v in calc_metrics(pred, label).items():
                    loss[k + "_" + name] = v

        return loss
