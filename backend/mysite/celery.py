import os
from celery import Celery
import django

# 设置默认的Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 初始化Django应用
django.setup()

app = Celery('mysite')

# 使用Django的设置文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 导入定时任务配置
from tasks.celery_beat_schedule import CELERY_BEAT_SCHEDULE
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

# 自动发现任务
app.autodiscover_tasks(['tasks'])

# 手动导入任务以确保它们被注册
try:
    from tasks.document_scan import scan_and_process_documents, process_document
    print(f"成功导入任务: {scan_and_process_documents}, {process_document}")
except ImportError as e:
    print(f"导入任务失败: {e}")

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
