# -*- encoding: utf-8 -*-
"""
@File    : inference.py
@Time    : 2019/10/30
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import multiprocessing
import os
import sys
from os.path import join as opj

import lmdb
import numpy as np
import torch
from torch import nn
from torchvision import transforms
from torchvision.datasets.folder import default_loader
from tqdm import tqdm

from utils.modeling.baseline import Baseline

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class FeatsLmdb:
    def __init__(self, lmdb_path="lmdb", map_size=int(1e8)):
        self._is_close = True
        self.env, self.txn = None, None
        self.db_file = lmdb_path
        self.map_size = map_size
        self.initialize()

    def add_item(self, image_id, vector):
        if self._is_close:
            self.initialize()
        self.txn = self.env.begin(write=True)
        self.txn.put(str(image_id).encode(), value=vector)
        self.txn.commit()

    def add_items(self, keys, vectors):
        if self._is_close:
            self.initialize()
        self.txn = self.env.begin(write=True)
        for index, key in enumerate(keys):
            self.txn.put(str(key).encode(), value=vectors(index))
        self.txn.commit()
        print("Successfully added %d items!" % (len(keys)))

    def delete_item(self, image_id):
        if self._is_close:
            self.initialize()
        self.txn = self.env.begin(write=True)
        self.txn.delete(str(image_id))
        self.txn.commit()

    def delete_items(self, image_ids):
        if self._is_close:
            self.initialize()
        self.txn = self.env.begin(write=True)
        for image_id in image_ids:
            self.txn.delete(str(image_id))
        self.txn.commit()
        print("Successfully deleted %d items!" % (len(image_ids)))

    def display(self):
        if self._is_close:
            self.initialize()
        self.txn = self.env.begin()
        cur = self.txn.cursor()
        print(cur)
        for key, value in cur:
            print(key, value)

    def initialize(self):
        # 数据库初始化
        self.env = lmdb.open(self.db_file, map_size=self.map_size)
        self._is_close = False

    def env_close(self):
        # 数据库关闭
        if not self._is_close:
            self.env.close()
            self._is_close = True

    def add_embed_to_lmdb(self, features, labels):
        assert len(features) == len(labels), "标签与特征数量不正确"
        for index, feat in enumerate(features):
            self.add_item(labels[index], feat.tostring())


def extract_feature(model, inputs):
    with torch.no_grad():
        input_img = inputs.to('cuda')
        outputs = model(input_img)
        features = torch.nn.functional.normalize(outputs, dim=1, p=2)
    return features.cpu().data.numpy()


def extract_feature_from_path(model, path):
    inputs = read_image(path)
    with torch.no_grad():
        input_img = inputs.to('cuda')
        outputs = model(input_img)
        features = torch.nn.functional.normalize(outputs, dim=1, p=2)
    return features.cpu().data.numpy()


def list_pictures(directory):
    imgs = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            imgs.append(opj(root, fname))
    return imgs


def read_image(img_path):
    img = default_loader(img_path)
    img = test_transform(img)
    img = img.unsqueeze(0)
    return img


def get_label(image_paths):
    id_list = []
    for image_path in image_paths:
        id_list.append(int(os.path.split(image_path)[1].split("_")[0]) + 1)
    return id_list


def get_model(model_path):
    model = Baseline(3519, 1, model_path, 'bnneck', 'before', 'resnet50', 'self')
    model = model.to('cuda')
    model = nn.DataParallel(model)
    resume = torch.load(model_path)
    model.load_state_dict(resume)
    model.eval()
    return model


def get_data_feature(model, data_dir):
    test_img_paths = [path for path in list_pictures(data_dir)]
    print(len(test_img_paths))
    batch_size = 64
    gf = np.zeros((len(test_img_paths), 1024))
    for i in tqdm(range(int(np.ceil(len(test_img_paths) / batch_size))), desc="图像特征提取"):
        cur_test_img = pool.map(read_image, test_img_paths[i * batch_size:(i + 1) * batch_size])
        cur_test_img = torch.cat(cur_test_img, 0)
        if len(cur_test_img) == 0: break
        cur_gf = extract_feature(model, cur_test_img)
        gf[i * batch_size:(i + 1) * batch_size, :] = cur_gf
    return gf


if __name__ == '__main__':
    model_path = '/home/public/competition_code/reid/AI-City-Vehicle-Reid/train/output/pretrain/center_range_50_acc745_best.pth'
    model = get_model(model_path)
    print('create multiprocessing...')
    pool = multiprocessing.Pool(processes=8)
    print('after create multiprocessing...')
    data_dir = '/home/public/reid/data/MVB_train/Image/probe_out'
    features = get_data_feature(model, data_dir)
    img_paths = [path for path in list_pictures(data_dir)]
    test_labels = np.asarray(get_label(img_paths))
    embed = FeatsLmdb()
    embed.add_embed_to_lmdb(features, test_labels)
    # embed.display()
    embed.env_close()
