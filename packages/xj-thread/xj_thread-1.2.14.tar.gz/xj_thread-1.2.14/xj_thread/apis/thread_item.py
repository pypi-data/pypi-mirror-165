"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块单挑数据删除/修改/详情
"""
from rest_framework.views import APIView

from xj_thread.services.thread_item_service import ThreadItemService
from xj_thread.utils.custom_authentication_wrapper import authentication_wrapper
from xj_thread.utils.model_handle import parse_data
from ..utils.custom_response import util_response

item_service = ThreadItemService()


class ThreadItemlAPI(APIView):
    """单挑信息处理，查，改，删"""

    def get(self, request, pk, *args, **kwargs):
        """信息表详情"""
        if not pk:
            return util_response(msg="非法请求", err=2554)
        data, error_text = item_service.detail(pk)

        if not error_text:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)

    @authentication_wrapper
    def put(self, request, pk, *args, **kwargs):
        """信息表编辑"""
        if not pk:
            return util_response(msg="非法请求", err=2554)
        form_data = parse_data(request=request)
        data, error_text = item_service.edit(form_data, pk)
        if not error_text:
            return util_response()
        return util_response(err=47767, msg=error_text)

    @authentication_wrapper
    def delete(self, request, pk, *args, **kwargs):
        data, error_text = item_service.delete(pk)
        print(error_text)
        if not error_text:
            return util_response()
        return util_response(err=47767, msg=error_text)
