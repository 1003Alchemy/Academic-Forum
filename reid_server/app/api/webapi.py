# -*- encoding: utf-8 -*-
"""
@File    : webapi.py
@Time    : 2019/10/23
@Author  : zlp
@Email   : zlp5icv@gmail.com
"""
from flask_restful.reqparse import RequestParser
from flask_restful import Resource
from app.tools.util import decode_image, is_base64
from app.tools.apiResult import generate_response
from app import model
from utils.inference import extract_feature


class Search(Resource):
    def __init__(self):
        self.req_parse = RequestParser()
        self.req_parse.add_argument("image", type=str, help='缺少该参数', required=True)
        super(Search, self).__init__()
    def get(self):
        # 设置api请求类型
        results_data = {"type": "search"}
        req = self.req_parse.parse_args(strict=True)
        # 获取请求参数
        image = req.get("image")
        # 判断图片是否base64编码
        if is_base64(image):
            # 解码图片
            img_data = decode_image(image)
            with open('static/temp/temp.jpg', 'wb') as f:
                f.write(img_data)
            if img_data:
                # todo 图片推理
                extract_feature(model, "static/temp/temp.jpg")
                results_data["class_dict"] = {}
                results_data["score_dict"] = {}
                results_data["clas_name_dict"] = {}
        return generate_response(results=results_data)


class Upload(Resource):
    def __init__(self):
        self.req_parser = RequestParser()
        self.req_parser.add_argument("image", type=str, location="args", required=True)
        self.req_parser.add_argument("class_id", type=int, location="args", required=True)

    def get(self):
        req = self.req_parser.parse_args(strict=True)
        image = req.get("image")
        image = req.get("image_id")
        image = req.get("class_id")
        if len(image):
            decode_image(image)
        return generate_response(data={"id": id})
