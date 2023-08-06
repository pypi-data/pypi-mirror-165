# ConvNeXt--Unet
Unet model with ConvNext as its encoder.

:construction: Work in progress...

## Roadmap
- [x] Source Code
- [ ] Document\
...

## Usage
```python
from convnext_unet import ConvNeXtUnet

model = ConvNeXtUnet(num_classes=1, encoder_name='convnext_tiny', activation='sigmoid', pretrained=False, in_22k=False)
```
`num_calsses`: number of output classes.\
`encoder_name`: name of encoder in `convnext_tiny`, `convnext_small`, `convnext_base`, `convnext_large`, `convnext_xlarge`.\
`activation`: activation function to call before output.\
`pretrained`: Whether to load ImageNet pretrained model for encoder.\
`in_22k`: Whether to load ImageNet-22k pretrained model for encoder.

## Acknowledgement
This repository is built on top of [Pytorch-UNet](https://github.com/milesial/Pytorch-UNet), [ConvNeXt](https://github.com/facebookresearch/ConvNeXt) and [
segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch).

## Copyright
This project is released under the GPL-3.0 license. Please see the [LICENSE](LICENSE) file for more information.\
Copyright (c) 2022 Tianyi Wang.\
All rights reserved.

This program incorporates a modified version of Other Program.\
Copyright (c) 2022 Meta Platforms, Inc. and affiliates.\
Copyright (c) 2022 milesial.\
Copyright (c) 2022 Pavel Iakubovskii.

## Citation
```
@Article{liu2022convnet,
  author  = {Zhuang Liu and Hanzi Mao and Chao-Yuan Wu and Christoph Feichtenhofer and Trevor Darrell and Saining Xie},
  title   = {A ConvNet for the 2020s},
  journal = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year    = {2022},
}

@inproceedings{ronneberger2015u,
  title={U-net: Convolutional networks for biomedical image segmentation},
  author={Ronneberger, Olaf and Fischer, Philipp and Brox, Thomas},
  booktitle={International Conference on Medical image computing and computer-assisted intervention},
  pages={234--241},
  year={2015},
  organization={Springer}
}
```