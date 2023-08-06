# Copyright (c) OpenMMLab. All rights reserved.
from .diff_mutable_module import (DiffChoiceRoute, DiffMutableModule,
                                  DiffMutableOP)
from .mutable_module import MutableModule
from .one_shot_mutable_module import OneShotMutableModule, OneShotMutableOP

__all__ = [
    'DiffMutableModule', 'DiffMutableOP', 'DiffChoiceRoute',
    'OneShotMutableOP', 'OneShotMutableModule', 'MutableModule'
]
