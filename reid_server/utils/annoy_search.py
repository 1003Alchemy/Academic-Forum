# -*- encoding: utf-8 -*-
"""
@File    : annoy_search.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from annoy import AnnoyIndex
import logging
import lmdb
import os
from utils.tools import embed2str, str2embed


class AnnoySearch:
    def __init__(self, vec_dim=2048, lmdb_file="static/lmdb", ann_file="static/annoy_file/tree.ann", metric='angular',
                 num_trees=10):
        self.vec_dim = vec_dim  # 要index的向量维度
        self.metric = metric  # 度量可以是"angular"，"euclidean"，"manhattan"，"hamming"，或"dot"
        self.annoy_instance = AnnoyIndex(self.vec_dim, self.metric)
        self.lmdb_file = lmdb_file
        self.ann_file = ann_file
        self.num_trees = num_trees
        self.logger = logging.getLogger('AnnoySearch')

    def save_annoy(self):
        self.annoy_instance.save(self.ann_file)
        self.logger.info('save annoy SUCCESS !')

    def unload_annoy(self):
        self.annoy_instance.unload()

    def load_annoy(self):
        try:
            self.annoy_instance.unload()
            self.annoy_instance.load(self.ann_file)
            self.logger.info('load annoy SUCCESS !')
        except FileNotFoundError:
            self.logger.error('annoy file DOES NOT EXIST , load annoy FAILURE !', exc_info=True)
        # 创建annoy索引

    def create_index_from_lmdb(self):
        # 遍历
        lmdb_file = self.lmdb_file
        if os.path.isdir(lmdb_file):
            evn = lmdb.open(lmdb_file)
            wfp = evn.begin()
            for key, value in wfp.cursor():
                key = int(key)
                value = str2embed(value)
                print(len(value))
                self.annoy_instance.add_item(key, value)

            self.annoy_instance.build(self.num_trees)
            self.annoy_instance.save(self.ann_file)

    def build_annoy(self):
        self.annoy_instance.build(self.num_trees)

    def get_nns_by_item(self, index, nn_num, search_k=-1, include_distances=False):
        return self.annoy_instance.get_nns_by_item(index, nn_num, search_k, include_distances)

    def get_nns_by_vector(self, vec, nn_num, search_k=-1, include_distances=False):
        return self.annoy_instance.get_nns_by_vector(vec, nn_num, search_k, include_distances)

    def get_n_items(self):
        return self.annoy_instance.get_n_items()

    def get_n_trees(self):
        return self.annoy_instance.get_n_trees()

    def get_vec_dim(self):
        return self.vec_dim

    def add_item(self, index, vec):
        self.annoy_instance.add_item(index, vec)

    def get_item_vector(self, index):
        return self.annoy_instance.get_item_vector(index)


if __name__ == '__main__':

    import random
    import time
    start=time.clock()
    ann_s = AnnoySearch(2048)
    ann_s.create_index_from_lmdb()
    ann_s.load_annoy()
    res = ann_s.get_nns_by_vector([random.gauss(0, 1) for z in range(2048)], 2)
    print(res)
    print(time.clock()-start)
    print(ann_s.get_item_vector(res[0]))
    print(ann_s.get_n_items())
    print(ann_s.get_vec_dim())
