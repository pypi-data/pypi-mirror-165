# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
import datetime
import logging

from django.core.paginator import Paginator
from django.db.models import F, Q
from rest_framework import serializers as serial

from xj_thread.services.thread_extend_service import ThreadExtendOutPutService
from ..models import Thread
from ..models import ThreadTagMapping

log = logging.getLogger()


# 信息服务CURD(支持扩展字段配置)
class ThreadListService:
    @staticmethod
    def list(params):
        page = params.get('page', 1)
        size = params.get('size', 20)
        tag_id_list = params.get('tag_id_list') if params.get('tag_id_list') else None  # 列表[1,2,3,4]
        # tag_value_list = params.get('tags', '').split(',')  # 列表['同城', '圣诞节']查询不用这个

        exclude_category_list = params.get('exclude_categorys').split(',') if params.get('exclude_categorys') else None
        # 边界检查：时间格式验证
        try:
            if params.get('start_time'):
                datetime.datetime.strptime(params.get('start_time'), "%Y-%m-%d %H:%M:%S")
            if params.get('end_time'):
                datetime.datetime.strptime(params.get('end_time'), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None, f'时间格式错误:它的格式应该是YYYY-MM-DD HH:MM:SS'

        # 允许进行过渡的字段条件
        conditions = {
            "category_id": params.get('category_id'),
            "category_id__value": params.get('category_value'),
            "classify_id": params.get('classify_id'),
            "classify_id__value": params.get('classify_value'),
            "title__icontains": params.get('title'),
            "create_time__gte": params.get('start_time'),
            "create_time__lte": params.get('end_time'),
            "user_id": params.get('user_id'),
            "user_id__in": params.get('user_id__in'),
            "user_id__not_in": params.get("user_id__not_in"),
            "is_deleted": False,
        }
        conditions = {k: v for k, v in conditions.items() if v or v is False or v == []}
        thread_set = Thread.objects
        if conditions.get("user_id__not_in"):
            thread_set = thread_set.filter(~Q(user_id__in=conditions.pop("user_id__not_in")))

        # 边界检查，不写这行，当size为0时，页面会报分母不能为零
        if int(size) <= 0:
            raise serial.ValidationError(f'请求每页数量(size)不能为零。')

        # 另一个条件查询的生成语句
        # keys = 'category_id__value classify_id classify_id__value title__icontains content__icontains create_time__gte create_time__lte is_deleted user_id'.split()
        # values = [category_value, classify_id, classify_value, title, content, start_time, end_time, is_deleted, user_id]
        # conditions = {k: v for k, v in zip(keys, values) if v or v is False}

        # 开始按过滤条件
        try:
            thread_set = thread_set.filter(**conditions)
            thread_set = thread_set.annotate(category_value=F("category_id__value")).values("category_value").annotate(classify_value=F("classify_id__value")) \
                .annotate(show_value=F("show_id__value")).annotate(auth_value=F("auth_id__value"))
            thread_set.annotate(views=F("show_id__value"))
            thread_set = thread_set.values('id',
                                           'category_id',
                                           'category_value',
                                           'classify_id',
                                           'classify_value',
                                           'show_id',
                                           'show_value',
                                           'user_id',
                                           'author',
                                           'auth_id',
                                           'auth_value',
                                           'title',
                                           'summary',
                                           'ip',
                                           'has_enroll',
                                           'has_fee',
                                           'has_comment',
                                           'cover',
                                           'photos',
                                           'video',
                                           'files',
                                           'price',
                                           'is_original',
                                           'more',
                                           'create_time',
                                           'update_time',
                                           )
        except Exception as e:
            return None, e.__str__()

        # 指定不需要过滤的类别字段
        if exclude_category_list:
            thread_set = thread_set.exclude(category_id__in=exclude_category_list)
        count = thread_set.count()
        # 这里先处理标签查询
        if tag_id_list:
            try:
                thread_id_list = ThreadTagMapping.objects.filter(tag_id__in=tag_id_list).values_list('thread_id', flat=True)  # flat转列表形式
                thread_set = thread_set.filter(id__in=thread_id_list)
            except ValueError as e:
                log.error(f'信息表标签查询{e}')
        # 分页数据
        finish_set = list(Paginator(thread_set, size).page(page))
        # 主键提取获取 扩展数据(thread_extends)# 扩展字段拼装服务
        category_id_list = list(set([item['category_id'] for item in finish_set if item['category_id']]))
        thread_id_list = list(set([item['id'] for item in finish_set if item['id']]))
        # 扩展数据拼接
        extend_merge_service = ThreadExtendOutPutService(category_id_list=category_id_list, thread_id_list=thread_id_list)
        finish_set = extend_merge_service.merge(finish_set)
        return {'list': finish_set, 'size': int(size), 'page': int(page), 'total': count}, None
