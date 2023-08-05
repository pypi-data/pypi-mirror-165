# coding=utf-8
import base64
import hashlib
import os
import re
import time
import configparser
from pathlib import Path

from rest_framework import serializers
from xj_resource.utils.model_handle import parse_model

from ..models import ResourceImage
from ..utils.digit_algorithm import DigitAlgorithm
from config.config import Config
from utils.x_dict import XDict
from utils.x_config import XConfig


# # 用于异常处理
# def robust(actual_do):
#     def add_robust(*args, **keyargs):
#         try:
#             return actual_do(*args, **keyargs)
#         except Exception as e:
#             print(str(e))
#
#     return add_robust


# 声明序列化，处理处理数据并写入数据
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceImage
        # 序列化验证检查，检查必填项的字段
        fields = ['id', 'group_id', 'user_id', 'title', 'url', 'filename', 'format', 'size', 'thumb', 'md5', 'snapshot', 'counter']


class ResourceImageService:

    def __init__(self):
        pass

    @staticmethod
    def create(params):
        # print("> create:", params)
        # # 检查MD5是否有历史上传记录
        # md5 = params.get('md5', None)
        # if md5 is None:
        #     return False
        # instance = ResourceImage.objects.filter(md5=md5).first()
        # if instance:
        #     return instance, None

        serializer = UploadImageSerializer(data=params)
        if not serializer.is_valid():
            return None, serializer.errors

        instance = serializer.save()
        return instance, None