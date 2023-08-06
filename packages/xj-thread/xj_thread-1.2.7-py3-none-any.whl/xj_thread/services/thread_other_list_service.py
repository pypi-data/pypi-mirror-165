"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块逻辑处理
"""
import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import F
from rest_framework import serializers

from ..models import ThreadAuth
from ..models import ThreadCategory
from ..models import ThreadClassify
from ..models import ThreadExtendField
from ..models import ThreadShow
from ..models import ThreadTag
from ..serializers import ThreadAuthListSerializer
from ..serializers import ThreadCategoryListSerializer
from ..serializers import ThreadTagSerializer

log = logging.getLogger()


class ThreadOtherListServices:
    def __init__(self):
        pass

    @staticmethod
    def thread_category():
        """
        类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
        """
        thread_category_obj = ThreadCategory.objects.all()
        res = ThreadCategoryListSerializer(thread_category_obj, many=True)
        return res.data, None

    @staticmethod
    def thread_classify(category_value=None, category_id=None, ):
        """
        分类。具体的分类，可以是按行业、兴趣、学科的分类，是主类别下的子分类。
        """
        classify_set = ThreadClassify.objects.all()
        if category_id:
            classify_set = classify_set.filter(category_id=category_id)
        if category_value:
            classify_set = classify_set.filter(category_id__value=category_value)
        classify_set = classify_set.annotate(category_value=F('category_id__value'))
        classify_set = classify_set.annotate(show_value=F('show_id__value'))
        # res = ThreadClassifyListSe0rializer(thread_classify_set, many=True)
        return list(classify_set.values()), None

    @staticmethod
    def thread_show(params=None):
        """
        展示类型。用于对前端界面的显示样式进行分类
        """
        thread_show_obj = list(ThreadShow.objects.annotate(label=F("value")).all().values("id", "label", "config", "description"))
        return thread_show_obj, None

    @staticmethod
    def thread_auth(params=None):
        """
        访问权限。作者指定允许哪里用户可以访问，例如私有、公开、好友、指定某些人可以访问等。
        """
        thread_auth_obj = ThreadAuth.objects.all()
        res = ThreadAuthListSerializer(thread_auth_obj, many=True)
        return res.data, None

    @staticmethod
    def thread_tag(params):
        """
        标签类型，存放预置标签。
        """
        size = params.get('size', 10)
        page = params.get('page', 1)
        thread_tag_obj = ThreadTag.objects.all()
        paginator = Paginator(thread_tag_obj, size)
        try:
            thread_tag_obj = paginator.page(page)
        except PageNotAnInteger:
            thread_tag_obj = paginator.page(1)
        except EmptyPage:
            thread_tag_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            log.error(f'信息主表分页:{str(e)}')
            raise serializers.ValidationError(str(e))
        res = ThreadTagSerializer(thread_tag_obj, many=True)
        data = {'total': paginator.count, 'list': res.data}
        return data, None

    @staticmethod
    def thread_extend_field_list(classify_id=None):
        """获取所有的扩展字段列表"""
        obj_list = ThreadExtendField.objects.annotate(field_label=F("value")).values("field", 'field_label', 'category_id', 'type', 'unit')
        if not classify_id is None:
            if type(classify_id) is list or type(classify_id) is tuple:
                obj_list = obj_list.filter(classify_id__in=classify_id)
            else:
                obj_list = obj_list.filter(classify_id=classify_id)
        return list(obj_list), None
