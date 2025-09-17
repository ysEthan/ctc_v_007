"""
Celery Beat 定时任务配置
"""
from celery.schedules import crontab

# 定时任务配置
CELERY_BEAT_SCHEDULE = {
    # 文档扫描任务 - 每6小时执行一次
    'scan-documents': {
        'task': 'tasks.document_scan.scan_and_process_documents',
        'schedule': crontab(minute=0, hour='*/6'),  # 每6小时的整点执行
        'options': {
            'queue': 'default',
            'routing_key': 'scan.documents',
        }
    },
    
    # 清理旧文档任务 - 每天凌晨2点执行
    'cleanup-old-documents': {
        'task': 'tasks.document_scan.cleanup_old_documents',
        'schedule': crontab(minute=0, hour=2),  # 每天凌晨2点执行
        'options': {
            'queue': 'default',
            'routing_key': 'cleanup.documents',
        }
    },
}
