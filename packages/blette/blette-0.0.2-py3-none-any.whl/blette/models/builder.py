#!/usr/bin/env python3

import warnings

from mmcv.utils import Registry

from mmseg.models.builder import (
    MODELS,
    BACKBONES,
    NECKS,
    HEADS as MMSEG_HEADS,
)

BLETTE_MODELS = Registry("blette_models", parent=MODELS)
HEADS = BLETTE_MODELS
LOSSES = BLETTE_MODELS
DETECTORS = BLETTE_MODELS


def build_backbone(cfg):
    """Build backbone."""
    return BACKBONES.build(cfg)


def build_neck(cfg):
    """Build neck."""
    return NECKS.build(cfg)


def build_mmseg_head(cfg):
    """Build head."""
    return MMSEG_HEADS.build(cfg)


def build_head(cfg):
    """Build head."""
    return HEADS.build(cfg)


def build_loss(cfg):
    """Build loss."""
    return LOSSES.build(cfg)


def build_detector(cfg, train_cfg=None, test_cfg=None):
    if train_cfg is not None or test_cfg is not None:
        warnings.warn(
            "train_cfg and test_cfg is deprecated, " "please specify them in model",
            UserWarning,
        )
    assert (
        cfg.get("train_cfg") is None or train_cfg is None
    ), "train_cfg specified in both outer field and model field "
    assert (
        cfg.get("test_cfg") is None or test_cfg is None
    ), "test_cfg specified in both outer field and model field "
    return DETECTORS.build(
        cfg, default_args=dict(train_cfg=train_cfg, test_cfg=test_cfg)
    )
