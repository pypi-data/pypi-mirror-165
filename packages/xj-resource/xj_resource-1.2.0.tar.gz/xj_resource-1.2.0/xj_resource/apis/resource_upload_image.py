from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response

from xj_user.services.user_service import UserService
from ..models import *
from ..services.resource_upload_service import ResourceUploadService
from ..services.resource_image_service import ResourceImageService
from ..utils.model_handle import util_response, only_filed_handle, parse_model


class UploadImage(APIView):
    def post(self, request):
        # ========== 一、检查：验证权限 ==========
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return Response({'err': 6001, 'msg': '缺少Token', })
        user_serv, error_text = UserService.check_token(token)
        if error_text:
            return Response({'err': 6002, 'msg': error_text, })
        user_id = user_serv.get('user_id', None)
        if not user_id:
            return Response({'err': 7001, 'msg': "用户不存在", })

        # ========== 二、检查：必填性 ==========
        # 对应postman的Body的key=file，value=上传文件的名称 watermelonhh.jpg
        input_file = request.FILES.get("image")
        title = request.POST.get("title")
        group_id = request.POST.get('group_id', 0)
        # print("> UploadImage: user_id, title, group_id:", user_id, title, group_id)
        if input_file is None:
            return Response({'err': 2001, 'msg': '未选择上传图片', 'tip': '未选择上传图片', })

        # ========== 三、检查：内容的准确性 ==========
        upload_serv = ResourceUploadService()
        file_info, error_text = upload_serv.init(input_file, by_month=True, user_id=user_id, title=title,
                                                 group_id=group_id, limit_size=None)
        if error_text:
            return Response({'err': 4005, 'msg': error_text, })

        # 写入磁盘
        upload_serv.write()
        print("> UploadImage: upload_serv:", upload_serv)

        # 写入数据库
        image_instance, error_text = ResourceImageService.create(params=file_info)
        print("> UploadImage: image_instance:", image_instance)
        if error_text:
            return Response({'err': 4006, 'msg': error_text, })
        if image_instance:
            file_info['id'] = image_instance.id

        return Response({'err': 0, 'msg': 'OK', 'data': file_info})

    # 文件列表
    def get(self, request):
        params = request.query_params.copy()
        limit = params.pop('limit', 20)
        page = params.pop('page', 20)
        params = only_filed_handle(params, {
            "title": "title__contains",
            "filename": "filename_contains",
            "md5": "md5",
            "user_id": "user_id"
        }, None)
        list_obj = ResourceImage.objects.filter(**params)
        count = list_obj.count()
        res_set = Paginator(list_obj, limit).get_page(page)
        return util_response(data={'count': count, 'page': page, 'limit': limit, "list": parse_model(res_set)})
