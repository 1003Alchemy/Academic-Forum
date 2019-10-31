# -*- encoding: utf-8 -*-
"""
@File    : exts.py.py
@Time    : 2019/10/30
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
import multiprocessing
import os
import numpy as np
import torch
from torch import nn
from torchvision import transforms
from torchvision.datasets.folder import default_loader
from tqdm import tqdm
from config import config
from utils.modeling.baseline import Baseline


class Inference(object):
    def __init__(self):
        self.model_path = config['production'].CNN_MODEL_PATH
        self.model = self.get_model()

        self.test_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def load(self, model_path):
        self.model = model_path
        return self.get_model()

    def extract_feature_from_path(self, path):
        inputs = self.read_image(path)
        with torch.no_grad():
            input_img = inputs.to('cuda')
            outputs = self.model(input_img)
            features = torch.nn.functional.normalize(outputs, dim=1, p=2)
        return features.cpu().data.numpy().astype().astype(np.float32)

    def extract_feature(self, inputs):
        with torch.no_grad():
            input_img = inputs.to('cuda')
            outputs = self.model(input_img)
            features = torch.nn.functional.normalize(outputs, dim=1, p=2)
        return features.cpu().data.numpy().astype(np.float32)

    def read_image(self, img_path):
        img = default_loader(img_path)
        img = self.test_transform(img)
        img = img.unsqueeze(0)
        return img

    def list_pictures(self, directory):
        imgs = []
        for root, dirs, files in os.walk(directory):
            for fname in files:
                imgs.append(os.path.join(root, fname))
        return imgs

    def get_label(self, image_paths):
        id_list = []
        for image_path in image_paths:
            id_list.append(int(os.path.split(image_path)[1].split("_")[0]) + 1)
        return id_list

    def get_data_feature(self, data_dir):
        test_img_paths = [path for path in self.list_pictures(data_dir)]
        batch_size = 64
        gf = np.zeros((len(test_img_paths), 2048))
        for i in tqdm(range(int(np.ceil(len(test_img_paths) / batch_size))), desc="图像特征提取"):
            cur_test_img=[]
            for x in test_img_paths[i * batch_size:(i + 1) * batch_size]:
                cur_test_img .append( self.read_image(x))
            cur_test_img = torch.cat(cur_test_img, 0)
            cur_gf = self.extract_feature(cur_test_img)
            gf[i * batch_size:(i + 1) * batch_size, :] = cur_gf
        return gf

    def get_model(self):
        model = Baseline(3519, 1, self.model_path, 'bnneck', 'before', 'resnet50', 'self')
        model = model.to('cuda')
        model = nn.DataParallel(model)
        resume = torch.load(self.model_path)
        model.load_state_dict(resume)
        model.eval()
        return model


Inference_Tools = Inference()
