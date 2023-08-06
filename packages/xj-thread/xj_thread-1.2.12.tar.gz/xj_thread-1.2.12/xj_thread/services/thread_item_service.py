# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""

from ..models import Thread
from ..models import ThreadExtendData
from ..serializers import ThreadDetailSerializer
from ..services.thread_extend_service import ThreadExtendService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_model, format_params_handle


# 信息服务CURD(支持扩展字段配置)  V2版本
class ThreadItemService:
    @staticmethod
    def detail(pk):
        """获取信息内容"""
        thread_obj = Thread.objects.filter(id=pk, is_deleted=False).first()
        if thread_obj:  # 信息统计表更新数据
            StatisticsService.increment(thread_id=thread_obj.id, tag='views', step=1)
        else:
            return None, "数据不存在"
        res_set = dict(ThreadDetailSerializer(thread_obj).data)
        # 扁平化数据
        res_set.update(res_set.pop('statistic'))
        res_set.update(res_set.pop('thread_extends'))
        return res_set, 0

    @staticmethod
    def edit(form_data, pk):
        form_data.setdefault("id", pk)
        filter_filed_list = [  # 主表过滤字段
            "category_id", 'classify_id', 'show_id', 'user_id', 'auth_id', 'title', 'content', 'summary', 'ip', 'has_enroll', 'has_fee',
            'has_comment', 'cover', "video", "photos", 'files', "price", "author", "create_time", "logs", "more"
        ]
        # 主表修改
        main_res = Thread.objects.filter(id=pk)
        if not main_res:
            return None, "数据不存在，无法进行修改"
        try:
            main_form_data = format_params_handle(form_data.copy(), filter_filed_list=filter_filed_list)
            main_res.update(**main_form_data)
        except Exception as e:
            return None, "信息主表写入异常：" + str(e)
        # 扩展字段修改
        # 排除主表之外的字段，理论上就是扩展字段，接下来仅仅需要转换一下扩展字段
        except_main_form_data = format_params_handle(form_data.copy(), remove_filed_list=filter_filed_list)
        return ThreadExtendService.create_or_update(except_main_form_data, pk, main_form_data.get("category_id", None))

    @staticmethod
    def delete(id):
        main_res = Thread.objects.filter(id=id, is_deleted=0)
        if not main_res:
            return None, "数据不存在，无法进行修改"
        main_res.update(is_deleted=1)
        return None, None

    @staticmethod
    def select_extend(id):
        """单独查询 查询扩展字段"""
        return util_response(parse_model(ThreadExtendData.objects.filter(id=id)))
