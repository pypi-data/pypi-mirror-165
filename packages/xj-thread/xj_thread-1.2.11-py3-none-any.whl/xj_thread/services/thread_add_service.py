# encoding: utf-8
"""
@project: djangoModel->thread_add
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 信息添加接口服务
@created_time: 2022/8/8 13:36
"""

from .thread_extend_service import ThreadExtendService
from ..models import Thread
from ..utils.model_handle import format_params_handle


class ThreadAddService:
    @staticmethod
    def add(params):
        # 扩展字段与主表字段拆分
        # 开启事务，防止脏数据
        filter_filed_list = [  # 主表过滤字段
            "category_id", 'classify_id', 'show_id', 'user_id', 'auth_id', 'title', 'content', 'summary', 'ip', 'has_enroll', 'has_fee',
            'has_comment', 'cover', "video", "photos", 'files', "price", "author", "create_time", "logs", "more"
        ]
        # 主编篇插入
        main_form_data = format_params_handle(
            params.copy(), filter_filed_list=filter_filed_list, alias_dict={'category_id': 'category_id_id', 'classify_id': 'classify_id_id'}
        )
        instance = Thread.objects.create(**main_form_data)
        # 扩展表插入
        except_main_form_data = format_params_handle(params.copy(), remove_filed_list=filter_filed_list)
        ThreadExtendService.create_or_update(except_main_form_data, instance.id, main_form_data.get("category_id_id", None))
        return {"id": instance.id}, None
