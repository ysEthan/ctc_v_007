"""
ICC管理应用配置
"""
from django.apps import AppConfig


class IccConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ICC'
    verbose_name = 'ICC管理'
