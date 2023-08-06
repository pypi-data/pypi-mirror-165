from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xj_role'
    verbose_name = '权限系统'
    sort = 1.1
