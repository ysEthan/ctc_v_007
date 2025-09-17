"""
用量管理应用配置
"""
from django.apps import AppConfig


class UsageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Usage'
    verbose_name = '用量管理'
