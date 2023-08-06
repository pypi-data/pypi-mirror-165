# encoding: utf-8
"""
@project: djangoModel->urls
@author: 孙楷炎
@synopsis: 运行目录URL
@created_time: 2022/7/6 9:51
"""

from django.conf.urls import url

from .apis.api import *

urlpatterns = [
    # 任务列表
    url(r'task_list/?$', TaskList.as_view()),
    url(r'task_add/?$', TaskAdd.as_view()),
    url(r'task_del/?$', TaskDel.as_view()),
    url(r'task_update/?$', TaskUpdate.as_view()),

    # 分组 分类
    url(r'group_list/?$', TaskGroupList.as_view()),
    url(r'group_add/?$', TaskGroupAdd.as_view()),
    url(r'group_del/?$', TaskGroupDel.as_view()),
    url(r'group_update/?$', TaskGroupUpdate.as_view()),

    # 指派用户
    url(r'appoint/?$', TaskAppoint.as_view()),
]
