# encoding: utf-8
"""
@project: djangoModel->user_list
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息列表
@created_time: 2022/7/25 9:42
"""
from rest_framework.views import APIView

from ..services.user_service import UserService
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data


class UserListAPIView(APIView):
    # 在有的框架中会出现传入3个参数的问题，原因不明，可能和两边使用的版本不同有关
    def get(self, request, *args):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        only_field_dict = {
            "page": "page",
            "size": "size",
            "user_id": "id",
            "email": "email",
            "full_name": "full_name__full_name",
            "user_name": "user_name__contains",
            "nickname": "nickname__contains",
        }
        params = parse_data(request, only_field=only_field_dict)
        data, err_txt = UserService.user_list(params)
        if not error_text:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)
