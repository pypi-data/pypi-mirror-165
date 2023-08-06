# encoding: utf-8
"""
@project: djangoModel->thread_add
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 信息添加接口
@created_time: 2022/8/8 13:36
"""
from rest_framework.views import APIView

from xj_thread.services.thread_add_service import ThreadAddService
from xj_thread.utils.model_handle import parse_data, util_response
from xj_thread.validator import ThreadAddValidator


class ThreadAdd(APIView):
    def post(self, request):
        params = parse_data(request)
        # # 表单初步验证
        validator = ThreadAddValidator(params)
        is_pass, error = validator.validate()
        if not is_pass:
            return util_response(err=4022, msg=error)
        # 插入服务
        data, err_txt = ThreadAddService.add(params)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
