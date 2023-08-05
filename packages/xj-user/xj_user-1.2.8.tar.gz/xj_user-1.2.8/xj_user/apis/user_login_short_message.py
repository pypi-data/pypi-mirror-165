import json

from django.http import HttpResponse
from rest_framework import response
from rest_framework.views import APIView
from django.core.cache import cache

from xj_user.services.user_service import UserService


class ShortMessageLogin(APIView):
    # 短信验证码校验
    def post(self, request):
        # 1. 电话和手动输入的验证码
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        # 2. 获取redis中保存的code
        # print('缓存中是否包含:', cache.has_key(phone))
        # print('取值:', cache.get(phone))
        cache_code = cache.get(phone)
        # 3. 判断
        account, error = UserService.check_account(phone)
        # print("账户：", account)
        if code == cache_code:
            auth_serv, error_text = UserService.check_login_short(user_id=account['user_id'], phone=account['phone'])
            if error_text:
                raise MyApiError(error_text, 6020)
            token = auth_serv['token']
            res = {
                'err': 0,
                'msg': 'OK',
                'data': {
                    'user_id': account['user_id'],
                    'token': token,
                },
            }
            headers = {
                "Authorization": token,
            }
            return response.Response(data=res, status=None, template_name=None, headers=headers, content_type=None)
        else:
            res = {
                'err': 4002,
                'msg': '验证码错误',
            }
            return response.Response(data=res, status=None, template_name=None)


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
