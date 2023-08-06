from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response

from xj_user.services.user_service import UserService
from ..models import *
from ..services.resource_upload_service import ResourceUploadService
from ..services.resource_image_service import ResourceImageService
from ..utils.model_handle import util_response, only_filed_handle, parse_model


class UploadList(APIView):
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
