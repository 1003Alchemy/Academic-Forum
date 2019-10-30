#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : siamese.py
@Time    : 2019/8/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
# encoding: utf-8
"""
@author:  liaoxingyu
@contact: sherlockliao01@gmail.com
"""

import torch
from torch import nn

from .backbones.resnet import ResNet, BasicBlock, Bottleneck
from .backbones.senet import SENet, SEResNetBottleneck, SEBottleneck, SEResNeXtBottleneck
from .backbones.densenet import densenet121,densenet161


def weights_init_kaiming(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_out')
        nn.init.constant_(m.bias, 0.0)
    elif classname.find('Conv') != -1:
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        if m.bias is not None:
            nn.init.constant_(m.bias, 0.0)
    elif classname.find('BatchNorm') != -1:
        if m.affine:
            nn.init.constant_(m.weight, 1.0)
            nn.init.constant_(m.bias, 0.0)


def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        nn.init.normal_(m.weight, std=0.001)
        if m.bias:
            nn.init.constant_(m.bias, 0.0)


class SiameseNetwork(nn.Module):
    in_planes = 2048

    # in_planes = 1024

    def __init__(self, num_classes, last_stride, model_path, neck, neck_feat, model_name, pretrain_choice):
        super(SiameseNetwork, self).__init__()
        if model_name == 'resnet18':
            self.in_planes = 512
            self.base = ResNet(last_stride=last_stride,
                               block=BasicBlock,
                               layers=[2, 2, 2, 2])
        elif model_name == 'resnet34':
            self.in_planes = 512
            self.base = ResNet(last_stride=last_stride,
                               block=BasicBlock,
                               layers=[3, 4, 6, 3])
        elif model_name == 'resnet50':
            self.base = ResNet(last_stride=last_stride,
                               block=Bottleneck,
                               layers=[3, 4, 6, 3])
        elif model_name == 'resnet101':
            self.base = ResNet(last_stride=last_stride,
                               block=Bottleneck,
                               layers=[3, 4, 23, 3])
        elif model_name == 'resnet152':
            self.base = ResNet(last_stride=last_stride,
                               block=Bottleneck,
                               layers=[3, 8, 36, 3])

        elif model_name == 'se_resnet50':
            self.base = SENet(block=SEResNetBottleneck,
                              layers=[3, 4, 6, 3],
                              groups=1,
                              reduction=16,
                              dropout_p=None,
                              inplanes=64,
                              input_3x3=False,
                              downsample_kernel_size=1,
                              downsample_padding=0,
                              last_stride=last_stride)
        elif model_name == 'se_resnet101':
            self.base = SENet(block=SEResNetBottleneck,
                              layers=[3, 4, 23, 3],
                              groups=1,
                              reduction=16,
                              dropout_p=None,
                              inplanes=64,
                              input_3x3=False,
                              downsample_kernel_size=1,
                              downsample_padding=0,
                              last_stride=last_stride)
        elif model_name == 'se_resnet152':
            self.base = SENet(block=SEResNetBottleneck,
                              layers=[3, 8, 36, 3],
                              groups=1,
                              reduction=16,
                              dropout_p=None,
                              inplanes=64,
                              input_3x3=False,
                              downsample_kernel_size=1,
                              downsample_padding=0,
                              last_stride=last_stride)
        elif model_name == 'se_resnext50':
            self.base = SENet(block=SEResNeXtBottleneck,
                              layers=[3, 4, 6, 3],
                              groups=32,
                              reduction=16,
                              dropout_p=None,
                              inplanes=64,
                              input_3x3=False,
                              downsample_kernel_size=1,
                              downsample_padding=0,
                              last_stride=last_stride)
        elif model_name == 'se_resnext101':
            self.base = SENet(block=SEResNeXtBottleneck,
                              layers=[3, 4, 23, 3],
                              groups=32,
                              reduction=16,
                              dropout_p=None,
                              inplanes=64,
                              input_3x3=False,
                              downsample_kernel_size=1,
                              downsample_padding=0,
                              last_stride=last_stride)
        elif model_name == 'senet154':
            self.base = SENet(block=SEBottleneck,
                              layers=[3, 8, 36, 3],
                              groups=64,
                              reduction=16,
                              dropout_p=0.2,
                              last_stride=last_stride)
        elif model_name == 'densenet121':
            self.base = densenet121(pretrained=False, progress=True)
        elif model_name == 'densenet161':
            self.base = densenet161(pretrained=False, progress=True)
        if pretrain_choice == 'imagenet':
            self.base.load_param(model_path)
            print('Loading pretrained ImageNet model {}......'.format(model_path))

        self.gap = nn.AdaptiveAvgPool2d(1)

        # self.part_gap = nn.MaxPool2d(kernel_size=(4, 16))
        # self.reduction1 = nn.Linear(self.in_planes, 512, bias=False)
        # self.reduction2 = nn.Linear(self.in_planes, 512, bias=False)
        # self.reduction3 = nn.Linear(self.in_planes, 512, bias=False)
        # self.reduction4 = nn.Linear(self.in_planes, 512, bias=False)

        # self.gap = nn.AdaptiveMaxPool2d(1)
        self.num_classes = num_classes
        # self.num_classes = 1434
        # self.num_classes = 10000
        # self.num_classes = 30000
        self.neck = neck
        self.neck_feat = neck_feat

        if self.neck == 'no':
            self.classifier = nn.Linear(self.in_planes, self.num_classes)
            # self.classifier = nn.Linear(self.in_planes, self.num_classes, bias=False)     # new add by luo
            # self.classifier.apply(weights_init_classifier)  # new add by luo
        elif self.neck == 'bnneck':
            self.bottleneck = nn.BatchNorm1d(self.in_planes)
            self.bottleneck.bias.requires_grad_(False)  # no shift
            self.classifier = nn.Linear(self.in_planes, self.num_classes, bias=False)

            self.bottleneck.apply(weights_init_kaiming)
            self.classifier.apply(weights_init_classifier)

    def forward(self, input1, input2):
        base_feat1 = self.base(input1)
        base_feat2 = self.base(input2)
        # part_feat = self.part_gap(base_feat)
        # part_feat1 = self.reduction1(part_feat[:, :, 0:1, :].squeeze(dim=3).squeeze(dim=2))
        # part_feat2 = self.reduction2(part_feat[:, :, 1:2, :].squeeze(dim=3).squeeze(dim=2))
        # part_feat3 = self.reduction3(part_feat[:, :, 2:3, :].squeeze(dim=3).squeeze(dim=2))
        # part_feat4 = self.reduction4(part_feat[:, :, 3:4, :].squeeze(dim=3).squeeze(dim=2))
        # global_feat = torch.cat([part_feat1, part_feat2, part_feat3, part_feat4], dim=1)

        global_feat1 = self.gap(base_feat1)  # (b, 2048, 1, 1)
        global_feat1 = global_feat1.view(global_feat1.shape[0], -1)  # flatten to (bs, 2048)

        global_feat2 = self.gap(base_feat2)  # (b, 2048, 1, 1)
        global_feat2 = global_feat2.view(global_feat2.shape[0], -1)  # flatten to (bs, 2048)
        # global_feat = torch.cat([global_feat1, global_feat2], dim=1)

        if self.neck == 'no':
            feat1 = global_feat1
            feat2 = global_feat2
        elif self.neck == 'bnneck':
            feat1 = self.bottleneck(global_feat1)  # normalize for angular softmax
            feat2 = self.bottleneck(global_feat2)  # normalize for angular softmax

        if self.training:
            feat = torch.cat([feat1, feat2], dim=1)
            global_feat = torch.cat([global_feat1, global_feat2], dim=1)
            cls_score = self.classifier(feat)
            return cls_score, global_feat  # global feature for triplet loss
        else:
            if self.neck_feat == 'after':
                # print("Test with feature after BN")
                feat = torch.cat([feat1, feat2], dim=1)
                return feat
            else:
                # print("Test with feature before BN")
                global_feat = torch.cat([global_feat1, global_feat2], dim=1)
                return global_feat

    def load_param(self, trained_path):
        param_dict = torch.load(trained_path)
        for key in param_dict:
            key_cut = key[7:]
            if 'classifier' in key_cut:
                continue
            self.state_dict()[key_cut].copy_(param_dict[key])
