# Copyright (c) 2022 Tianyi Wang
# All rights reserved.

# This source code is licensed under the GPL-3.0 license which can be found in the LICENSE file.



import torch.nn as nn

from .decoder import OutConv, Down, Up, DoubleConv
from . import encoder
from segmentation_models_pytorch.base.modules import Activation

ENCODERS = [
    'convnext_tiny', 'convnext_small', 'convnext_base', 'convnext_large', 'convnext_xlarge',
]
ENCODER_DIMS = {
    'convnext_tiny': [96, 192, 384, 768],
    'convnext_small': [96, 192, 384, 768],
    'convnext_base': [128, 256, 512, 1024],
    'convnext_large': [192, 384, 768, 1536],
    'convnext_xlarge': [256, 512, 1024, 2048],
}


class ConvNeXtUnet(nn.Module):
    def __init__(self, num_classes, encoder_name, pretrained=False, in_22k=False, activation=None, in_channels=3, bilinear=False, **kwargs):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.bilinear = bilinear
        dims = ENCODER_DIMS[encoder_name]
        self.in_conv = DoubleConv(self.in_channels, dims[0] // 2)

        try:
            encoder_model = getattr(encoder, encoder_name)
        except AttributeError:
            raise AttributeError(
                f"Wrong encoder name '{encoder_name}'. Available options are: {ENCODERS}"
            )

        self.convnext = encoder_model(pretrained, in_22k, **kwargs)

        self.up1 = Up(dims[3], dims[2], bilinear)
        self.up2 = Up(dims[2], dims[1], bilinear)
        self.up3 = Up(dims[1], dims[0], bilinear)
        self.up4 = Up(dims[0], self.in_channels, bilinear)
        self.outc = OutConv(self.in_channels, self.num_classes)
        self.activation = Activation(activation)

    def forward(self, x):
        x = self.in_conv(x)
        x, features = self.convnext(x)
        x = self.up1(x, features[3])
        x = self.up2(x, features[2])
        x = self.up3(x, features[1])
        x = self.up4(x, features[0])
        x = self.outc(x)
        return self.activation(x)
