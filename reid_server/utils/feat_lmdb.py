# -*- encoding: utf-8 -*-
"""
@File    : feat_lmdb.py
@Time    : 2019/10/24
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""

import lmdb
from utils.tools import str2embed, embed2str


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


def add_embed_to_lmdb(features, labels, embed_lmdb):
    assert len(features) == len(labels), "标签与特征数量不正确"
    for index, feat in enumerate(features):
        embed_lmdb.add_item(labels[i],feat.tostring())


if __name__ == '__main__':
    # 插入数据
    import numpy as np

    embed = FeatsLmdb()
    for i in range(50000):
        a = np.random.rand(128).astype(np.float32)
        embed.add_item(i, embed2str(a))
    embed.display()
    embed.env_close()
