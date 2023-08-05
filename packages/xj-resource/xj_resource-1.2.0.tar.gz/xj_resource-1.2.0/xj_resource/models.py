# coding=utf-8
from django.db import models
from django.utils import timezone


# ================================== 图片模块 模型=============================


class ResourceImageGroup(models.Model):
    class Meta:
        db_table = u'resource_image_group'
        verbose_name = '3.资源 - 图片分组表'
        verbose_name_plural = verbose_name

    group = models.CharField(verbose_name='图片组名', max_length=128, blank=True, null=True)
    title = models.CharField(verbose_name='图片组标题', max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name='图片组描述', max_length=225, blank=True, null=True)
    source_table = models.CharField(verbose_name='关联数据源表名', max_length=128, blank=True, null=True)


class ResourceImage(models.Model):
    class Meta:
        db_table = u'resource_image'
        verbose_name = '1.资源 - 图片表'
        verbose_name_plural = verbose_name

    group = models.ForeignKey(ResourceImageGroup, verbose_name='图片分组', db_column='group_id', blank=True, null=True, on_delete=models.DO_NOTHING)
    user_id = models.BigIntegerField(verbose_name='用户ID', db_column='user_id', db_index=True, blank=True, null=True)
    title = models.CharField(verbose_name='图片标题', max_length=255, blank=True, null=True)
    # url = models.ImageField(verbose_name='缩略图', upload_to="static/images", max_length=21845, blank=True, null=True, help_text='缩略图')
    url = models.CharField(verbose_name='图片链接', max_length=255, blank=True, null=True, db_index=True)
    filename = models.CharField(verbose_name='文件名', max_length=255, blank=True, null=True)
    format = models.CharField(verbose_name='文件类型', max_length=32)
    size = models.IntegerField(verbose_name='文件尺寸', blank=True, null=True)
    thumb = models.TextField(verbose_name='缩略图(Base64)', blank=True, null=True)
    md5 = models.CharField(verbose_name='MD5校验', max_length=255, blank=True, null=True)  # 判断使文件是否有效且唯一。
    snapshot = models.JSONField(verbose_name='文件快照', blank=True, null=True)  # for Python 3.8
    created_at = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='编辑时间', default=timezone.now)
    counter = models.IntegerField(verbose_name='使用计数器', blank=True, null=True)

    def __str__(self):
        return self.url

    @staticmethod
    def insert(data):
        try:
            res = ResourceImage.objects.create(**data)
            return res.id, None
        except Exception as e:
            return [], '写入异常' + str(e)
            # return [], '写入异常' + e.message


class ResourceImageMap(models.Model):
    class Meta:
        db_table = 'resource_image_map'
        verbose_name_plural = '2. 资源 - 图片映射表'

    image_id = models.ForeignKey(verbose_name='图片ID', to=ResourceImage, related_name='image_id_set+',
                                 on_delete=models.DO_NOTHING, db_column='image_id')
    source_id = models.BigIntegerField(verbose_name='来源ID', blank=True, null=True)
    source_table = models.CharField(verbose_name='来源表', max_length=128, blank=True, null=True)
    price = models.DecimalField(verbose_name='价格', max_digits=32, decimal_places=8, blank=True, null=True,
                                db_index=True)

    def __str__(self):
        return self.image_id


# =========================  文件模块 模型 ================

class ResourceFile(models.Model):
    class Meta:
        db_table = u'resource_file'
        verbose_name = '3.资源 - 文件表'
        verbose_name_plural = verbose_name

    user_id = models.BigIntegerField(verbose_name='用户', db_column='user_id', db_index=True)
    title = models.CharField(verbose_name='文件标题', max_length=255, blank=True, null=True)
    url = models.CharField(verbose_name='文件链接', max_length=255, blank=True, null=True, db_index=True)
    filename = models.CharField(verbose_name='文件名', max_length=255, blank=True, null=True)
    format = models.CharField(verbose_name='文件类型', max_length=32)
    thumb = models.TextField(verbose_name='缩略图', blank=True, null=True)
    md5 = models.CharField(verbose_name='MD5', max_length=255, blank=True, null=True)  # 判断使文件是否有效且唯一。
    # thumb = models.ImageField(verbose_name='缩略图', upload_to="static/images", max_length=21845, blank=True, null=True, help_text='缩略图')
    snapshot = models.JSONField(verbose_name='快照')

    def __str__(self):
        return self.id

    @staticmethod
    def insert(data):
        try:
            res = ResourceImage.objects.create(**data)
            return res.id, None
        except Exception as e:
            return [], '写入异常' + str(e)
            # return [], '写入异常' + e.message


class ResourceFileMap(models.Model):
    class Meta:
        db_table = 'resource_file_map'
        verbose_name_plural = '4. 资源 - 文件映射表'

    file_id = models.ForeignKey(verbose_name='文件ID', to=ResourceImage, related_name='file_id_set+',
                                on_delete=models.DO_NOTHING, db_column='file_id')
    source_id = models.BigIntegerField(verbose_name='来源ID', blank=True, null=True)
    source_table = models.CharField(verbose_name='来源表', max_length=128, blank=True, null=True)
    price = models.DecimalField(verbose_name='价格', max_digits=32, decimal_places=8, blank=True, null=True,
                                db_index=True)

    def __str__(self):
        return self.id
