"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块路由分发
"""
from django.urls import re_path

# from .apis.apis_v1 import ThreadListAPIView, ThreadDetailAPIView, AuthListAPIView, CategoryListAPIView, ClassifyListAPIView, ShowListAPIView, TagListAPIView
from .apis.thread_add import ThreadAdd
from .apis.thread_item import ThreadItemlAPI
from .apis.thread_list import ThreadListAPIView
from .apis.thread_other_list import AuthListAPIView, CategoryListAPIView, ClassifyListAPIView, ShowListAPIView, TagListAPIView, ThreadExtendFieldList
from .apis.thread_statistic import ThreadStaticAPIView

# 应用名称
# app_name = 'thread'

urlpatterns = [
    re_path(r'^category_list/?$', CategoryListAPIView.as_view(), name='category_list'),  # 类别列表
    re_path(r'^classify_list/?$', ClassifyListAPIView.as_view(), name='classify_list'),  # 分类列表
    re_path(r'^show_list/?$', ShowListAPIView.as_view(), name='show_list'),  # 展示类型列表
    re_path(r'^tag_list/?$', TagListAPIView.as_view(), name='tag_list'),  # 展示类型列表
    re_path(r'^list/?$', ThreadListAPIView.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item_add/?$', ThreadAdd.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item/(?P<pk>\d+)/?$', ThreadItemlAPI.as_view(), name='detail'),  # 信息单挑操作：详情/编辑/删除
    # 列表 信息相关
    re_path(r'^auth[_/]list/?$', AuthListAPIView.as_view(), name='auth_list'),  # 权限列表
    re_path(r'^extend_field_list/?$', ThreadExtendFieldList.as_view(), name='tag_list'),  # 展示类型列表
    re_path(r'^statistic/?$', ThreadStaticAPIView.as_view(), name='tag_list'),  # 计数统计，前端埋点接口
]
