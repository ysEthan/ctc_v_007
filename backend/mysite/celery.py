import os
from celery import Celery

# 设置默认的Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

# 使用Django的设置文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 导入定时任务配置
from tasks.celery_beat_schedule import CELERY_BEAT_SCHEDULE
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

# 自动发现任务
app.autodiscover_tasks(['tasks'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
