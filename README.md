# RE-ID图像检索系统
## server
- flask--REST-API
- lmdb--特征存储
- annoy--特征索引

app/viewers.py 主视图文件
app/models.py 数据库model以及操作函数
reid_server/utils/exts.py CNN相关函数
reid_server/utils/annoy_search.py annoy检索
reid_server/utils/feat_lmdb.py lmdb存储
reid_server/web_initialization.py 数据库初始化
reid_server/config.py 配置文件
reid_server/utils/modeling CNN模型