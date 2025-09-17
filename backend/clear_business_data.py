#!/usr/bin/env python
"""
清空业务相关数据库脚本
保留用户认证相关数据，清空业务数据
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import transaction
from django.apps import apps

def clear_business_data():
    """清空业务相关数据"""
    
    # 需要清空的业务模型
    business_models = [
        'ICC.ICC',
        'Subscription.Subscription', 
        'Usage.Usage',
        'document.Document',
        'document.BadCase',
        'django_celery_results.TaskResult',
        'django_celery_results.ChordCounter',
        'django_celery_results.GroupResult',
    ]
    
    # 保留的模型（用户认证相关）
    preserve_models = [
        'auth.User',
        'auth.Group',
        'auth.Permission',
        'authentication.User',
        'authentication.EmailVerification',
        'authentication.UserGroup',
        'authentication.LoginLog',
        'django_celery_beat.SolarSchedule',
        'django_celery_beat.IntervalSchedule',
        'django_celery_beat.ClockedSchedule',
        'django_celery_beat.CrontabSchedule',
        'django_celery_beat.PeriodicTasks',
        'django_celery_beat.PeriodicTask',
    ]
    
    print("开始清空业务数据...")
    
    with transaction.atomic():
        total_deleted = 0
        
        for model_path in business_models:
            try:
                app_label, model_name = model_path.split('.')
                model = apps.get_model(app_label, model_name)
                
                # 获取删除前的记录数
                count_before = model.objects.count()
                
                # 删除所有记录
                deleted_count, _ = model.objects.all().delete()
                
                total_deleted += deleted_count
                print(f"✅ {model_path}: 删除了 {deleted_count} 条记录")
                
            except Exception as e:
                print(f"❌ {model_path}: 删除失败 - {str(e)}")
        
        print(f"\n🎉 数据清理完成！总共删除了 {total_deleted} 条业务记录")
        print("\n保留的数据:")
        for model_path in preserve_models:
            try:
                app_label, model_name = model_path.split('.')
                model = apps.get_model(app_label, model_name)
                count = model.objects.count()
                print(f"  📊 {model_path}: {count} 条记录")
            except Exception as e:
                print(f"  ❌ {model_path}: 查询失败 - {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("数据库清理工具")
    print("=" * 60)
    print("⚠️  警告：此操作将清空所有业务数据！")
    print("✅ 保留：用户认证、登录日志、定时任务配置")
    print("🗑️  清空：ICC、Subscription、Usage、Document、BadCase、Celery任务结果")
    print("=" * 60)
    
    # 确认操作
    confirm = input("\n确认执行清理操作？(输入 'YES' 确认): ")
    
    if confirm == 'YES':
        clear_business_data()
    else:
        print("❌ 操作已取消")
