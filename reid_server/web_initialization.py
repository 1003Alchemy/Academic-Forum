# -*- encoding: utf-8 -*-
"""
@File    : web_initialization.py
@Time    : 2019/10/30
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from app import db, create_app, add_camera, add_image, add_class, select_image_by_id, select_image_by_path
import os
from utils.inference import get_data_feature, list_pictures, get_label
import multiprocessing
import numpy as np
import lmdb
from utils.annoy_search import AnnoySearch
import utils.exts

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
        for key, value in cur:
            print(key, len(value))

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


cam_list = {"g1": 1, "g2": 2, "g3": 3, "g4": 4, "p1": 5, "p2": 6, "p3": 7, "p4": 8}
app = create_app()
app_ctx = app.app_context()  # app_ctx = app/g
with app_ctx:  # __enter__,通过LocalStack放入Local中
    # 创建数据库
    # db.create_all()
    # # 导入摄像头数据
    # for i in range(len(cam_list)):
    #     add_camera(i + 1, "安检口" + str(i + 1), "192.168." + str(100 + i))
    # # 导入图片数据
    # cnt = 1
    # for root, dir, files in os.walk("/static/img_data"):
    #     class_f = False
    #     for file in files:
    #         image_path = os.path.join(os.path.split(root)[-1], file)
    #         class_id = int(os.path.split(root)[-1])
    #         class_name = str(os.path.split(root)[-1])
    #         date = "20191008104400"
    #         annoy_index = cnt
    #         cid = cam_list[file.split(".")[0].split("_")[1] + str(file.split(".")[0].split("_")[2])]
    #         if not class_f:
    #             add_class(class_id + 1, class_name)
    #             class_f = True
    #         add_image(image_path, class_id + 1, cid, annoy_index, date)
    #         cnt += 1
    # print("数据库导入完成！")
    data_dir = 'static/img_data'
    features = utils.exts.Inference_Tools.get_data_feature(data_dir)
    img_paths = [path for path in utils.exts.Inference_Tools.list_pictures(data_dir)]
    print("特征提取完成！")
    test_labels = np.asarray(utils.exts.Inference_Tools.get_label(img_paths))
    embed = FeatsLmdb(lmdb_path="static/lmdb")
    embed.add_embed_to_lmdb(features, test_labels)
    embed.display()
    embed.env_close()
    ann_s = AnnoySearch(2048)
    print("特征存储完成！")
    print("建立检索树...")
    ann_s.create_index_from_lmdb()
    print("检索树建立完成！")
    ann_s.load_annoy()
    print(ann_s.get_n_items())
