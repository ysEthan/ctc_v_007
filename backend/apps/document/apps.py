"""
文档管理应用配置
"""
from django.apps import AppConfig


class DocumentConfig(AppConfig):
    """
    文档管理应用配置
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.document'
    verbose_name = '文档管理'
    
    def ready(self):
        """
        应用准备就绪时的初始化
        """
        # 导入信号处理器
        try:
            import apps.document.signals
        except ImportError:
            pass