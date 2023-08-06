# coding=utf-8
import base64
import hashlib
import os
import re
import time
from pathlib import Path

from rest_framework import serializers

from ..models import ResourceImageGroup
from ..utils.digit_algorithm import DigitAlgorithm
from main.settings import BASE_DIR
from utils.x_dict import XDict
from utils.x_config import XConfig

module_dir = Path(__file__).parent.parent
root_config = XDict(XConfig.get_section(str(BASE_DIR) + '/config.ini', 'xj_resource', encode='utf-8-sig'))
module_config = XDict(XConfig.get_section(str(module_dir) + '/config.ini', 'xj_resource', encode='utf-8-sig'))


class ResourceUploadService:
    """
    @class 资源上传服务。
    @description 该服务只提供文件上传和生成信息，不提供数据库写入！
    """
    # 公共成员，基本数据
    user_id = None  # 用户ID
    title = None  # 文件标题
    filename = None  # 文件名
    url = None  # 文件地址
    suffix = None  # 文件类型
    size = None  # 文件尺寸
    thumb = None  # 缩略图(Base64)
    md5 = None  # MD5校验
    group_id = None  # 文件分组
    counter = None  # 计数器
    # 公共成员，允许类外编辑
    origin_title = None  # 原标题
    origin_filename = None  # 原文件名
    save_dir = None  # 保存目录
    pseudo_dir = None  # 伪静态目录
    save_absolute_dir = None  # 完整上传路径，包含文件名

    # 私有成员，仅限类内查看
    # 配置组
    __root_config = root_config  # 根配置，第一配置，
    __module_config = module_config  # 模块配置，第二配置
    __upload_dir = None  # 上传文件的写入目录。真实目录，因为大部分情况下，并不希望用户看到文件存放的真实路径
    __upload_url = None  # 上传文件的链接地址。虚拟目录，因为大部分情况下，并不希望用户看到文件存放的真实路径
    __upload_host = None  # 上传文件的主机
    __upload_format = None  # 支持的文件格式列表
    __upload_limit = None  # 上传文件大小限制，单位：字节

    __file_info = {}  # 文件 信息
    __input_file = None  # 上传文件
    __file_stream = None  # 上传文件流

    __error_message = None  # 异常消息

    # 构造函数，导入配置文件
    def __init__(self, upload_type='image'):
        """
        @param upload_type 上传文件类型。可选值：image, file, video。不同类型将分别上传至不同的文件夹。
        @description 待补充
        """
        c1 = self.__root_config
        c2 = self.__module_config

        if upload_type.strip().lower() == 'image':
            self.__upload_dir = c1.image_upload_dir or c2.image_upload_dir or "/media/upload/images/"
            self.__upload_url = c1.image_upload_url or c2.image_upload_url or "/media/images/"
            self.__upload_host = c1.image_host or c2.image_host or ""
            self.__upload_formats = c1.image_formats or c2.image_formats or None
            self.__upload_prefix = c1.image_prefix or c2.image_prefix or 'img_'
            self.__upload_limit = c1.image_limit or c2.image_limit or None

        if upload_type.strip().lower() == 'file':
            self.__upload_dir = c1.file_upload_dir or c2.file_upload_dir or "/media/upload/files/"
            self.__upload_url = c1.file_upload_url or c2.file_upload_url or "/media/files/"
            self.__upload_host = c1.file_host or c2.file_host or ""
            self.__upload_formats = c1.file_formats or c2.file_formats or None
            self.__upload_prefix = c1.image_prefix or c2.image_prefix or 'file_'
            self.__upload_limit = c1.file_limit or c2.file_limit or None

        if upload_type.strip().lower() == 'video':
            self.__upload_dir = c1.file_upload_dir or c2.file_upload_dir or "/media/upload/videos/"
            self.__upload_url = c1.file_upload_url or c2.file_upload_url or "/media/videos/"
            self.__upload_host = c1.file_host or c2.file_host or ""
            self.__upload_formats = c1.file_formats or c2.file_formats or None
            self.__upload_prefix = c1.image_prefix or c2.image_prefix or 'video_'
            self.__upload_limit = c1.file_limit or c2.file_limit or None

    # 初始化，基本信息、目录、文件等，初始化完成后可直接写入
    def init(self, input_file, by_month=False, user_id=None, title=None, group_id=None, limit_size=None):
        """
        初始化，基本信息、目录、文件等，初始化完成后可直接写入
        @param input_file {FILE} 输入文件。来自表单提交的FILE
        @param by_month {boolean} 按月分组存储。
        @param user_id {int} 用户ID。
        @param title {string} 文件标题。
        @param group_id {int} 分组ID。
        @param limit_size {int} 文件限制大小。
        @return file_info, error_text {tuple}
        @rtype tuple
        @type FIlE
        @note 待填写
        @author Ian.Sieyoo.Zhao
        @license MSI
        @contact sieyoo@163.com
        @version V1.2.0.20220828
        """
        if not input_file:
            return None, "请选择文件"
        # print("> init: __input_file:", input_file, type(input_file))

        # 先检查目录
        save_dir, error_text = self.init_dir(by_month=by_month)
        if error_text:
            return None, error_text
        # print("> init: save_dir:", save_dir)

        # 再检查文件
        self.__input_file = input_file
        self.user_id = user_id  # 用户ID
        self.title = title  # 文件标题
        self.group_id = group_id  # 分组ID
        self.__upload_limit = limit_size  # 上传限制大小，单位：字节
        file_info, error_text = self.init_file(file_title=title)
        # print("> init: file_info", file_info)
        if error_text:
            return None, error_text
        # print("> init: validate", file_info)

        return self.__file_info, None

    # 读取文件存放的目录，并根据by_month判断是否需要按月份做文件夹分组
    def init_dir(self, directory=None, by_month=False):
        """
        读取文件存放的目录，并根据by_month判断是否需要按月份做文件夹分组
        @param directory {string} 本地相对目录。相对于项目根目录。
        @param by_month {boolean} 按月分组存储。如果分组目录不存在则自动创建。
        @return save_dir, error_text {tuple} 文件目录，错误码
        @description 待填写
        """
        month = time.strftime('%Y-%m', time.localtime(time.time()))
        save_dir = directory
        pseudo_dir = self.__upload_url
        if not save_dir:
            save_dir = self.__upload_dir
        if by_month:
            save_dir = f"{save_dir}/{month}/".replace('//', '/')
            pseudo_dir = f"{pseudo_dir}/{month}/".replace('//', '/')

        # 不存在则创建目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # 再次检查目录存在
        if not os.path.exists(save_dir):
            return None, "目录创建失败，请检查是否有目录权限：" + save_dir

        # print("> init_dir: save_dir:", save_dir)
        self.save_dir = save_dir
        self.pseudo_dir = pseudo_dir
        return save_dir, None

    # 验证文件是否合法
    def init_file(self, file_title=None):
        """
        验证文件是否合法。
        @param file_title {string} 文件标题。修改文件生成的标题。
        @return file_info, error_text {tuple} 文件目录，错误码
        @description 验证文件是否合法，同时生成文件配置信息
        """
        # 一检查文件名
        self.origin_filename = self.__input_file.name
        ret = re.search(r'(.*)\.(\w{3,5})$', self.__input_file.name)
        if not ret:
            return None, '上传的文件名错误，格式后辍应为3-5个字符'
        self.origin_title = ret.group(1)
        self.suffix = ret.group(2)
        self.filename = f"{self.__upload_prefix}{DigitAlgorithm.make_unicode_16()}.{self.suffix}"
        self.save_absolute_dir = (str(BASE_DIR) + self.save_dir + self.filename).replace("//", "/")
        # print("> init_file: save_absolute_dir:", self.save_absolute_dir)

        # 二检查文件格式
        if self.__upload_formats and self.__upload_formats.strip() != '*' and self.suffix \
                and self.suffix not in self.__upload_formats.split(","):
            return None, '上传文件格式错误，支持：' + self.__upload_formats

        # 三检查文件流
        self.__file_stream = self.__input_file.read()
        if not self.__file_stream:
            return None, '文件流读取失败'

        # 四检查文件大小
        self.size = size = len(self.__file_stream)
        # print("> init_file: __file_stream", type(self.__file_stream), size)
        if size == 0:
            return None, "空文件"
        if self.__upload_limit and size > self.__upload_limit:
            return None, f"文件大小超过限制，不应大于{self.__upload_limit}字节。"

        # 五生成文件信息
        if self.group_id:
            check_group_id = ResourceImageGroup.objects.filter(id=self.group_id)
            if not check_group_id:
                self.group_id = None
        self.__file_info['group_id'] = self.group_id
        self.__file_info['user_id'] = self.user_id
        self.__file_info['title'] = self.title = file_title if file_title else self.origin_title
        self.__file_info['filename'] = self.filename
        self.__file_info['url'] = self.url = f"{self.__upload_host}{self.pseudo_dir}{self.filename}"
        self.__file_info['format'] = self.suffix
        self.__file_info['size'] = self.size
        self.__file_info['thumb'] = None
        self.__file_info['md5'] = self.md5 = self.get_md5()
        self.__file_info['snapshot'] = {
            'origin_filename': self.origin_filename,
            'upload_host': self.__upload_host,
            'upload_url': self.__upload_url,
            # 'pseudo_dir': self.pseudo_dir,
            # 'save_dir': self.save_dir,  # 不放快照，因为大部分情况下，并不希望用户看到文件存放的真实路径
        }
        self.__file_info['counter'] = 1
        print("> init_file: __file_info:", self.__file_info)
        return self.__file_info, None

    def get_md5(self):
        """
        获取文件MD5校验码。
        @return md5 {string} MD5校验码
        @description 略
        """
        content_md5 = hashlib.md5()
        content_md5.update(self.__file_stream)
        content_base64 = base64.b64encode(content_md5.digest())
        return content_base64.decode("utf-8")

    def write(self, target='disk'):
        """
        写入文件
        @return target {string} 写入目标。可选值：disk, oss。
        @description 略
        """
        if target == 'disk':
            self.write_disk()
        if target == 'oss':
            self.write_oss()

    def write_disk(self):
        try:
            # 文件写入磁盘
            # print("> write_disk: save_absolute_path:", self.save_absolute_dir)
            with open(self.save_absolute_dir, 'wb') as f:
                f.write(self.__file_stream)
        except Exception as e:
            # print("> write_disk Exception:", e)
            pass

    def write_oss(self, config):
        # 写入云存储
        pass
