"""
订阅管理应用配置
"""
from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Subscription'
    verbose_name = '订阅管理'
