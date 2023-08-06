# _*_coding:utf-8_*_

from django.urls import re_path

from xj_role.apis.permission_api import PermissionsAPIView
from xj_role.apis.role_api import RoleAPIView

app_name = 'xj_role'

# 应用路由
urlpatterns = [
    # 角色接口
    re_path(r'^tree/?$', RoleAPIView.tree),
    re_path(r'^list/?$', RoleAPIView.list),

    # 权限接口
    re_path(r'^permission/?$', PermissionsAPIView.as_view(), ),
    re_path(r'^permission_list/?$', PermissionsAPIView.list, ),
]
