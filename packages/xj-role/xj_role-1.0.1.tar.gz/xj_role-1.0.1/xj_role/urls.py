# _*_coding:utf-8_*_

from django.urls import re_path

# from django.urls import include
# from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
from .apis import user_permission

# 应用名称
app_name = 'xj_role'

# 应用路由
urlpatterns = [
    re_path(r'^permission/?$', user_permission.UserPermissions.as_view(), ),
]
