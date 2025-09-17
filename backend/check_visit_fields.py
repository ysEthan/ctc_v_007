#!/usr/bin/env python
"""
检查visitMcc和visitMnc字段的脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from apps.Usage.models import Usage

def check_visit_fields():
    """检查visitMcc和visitMnc字段"""
    try:
        print("=== 检查visitMcc和visitMnc字段 ===")
        
        # 1. 检查总记录数
        total_count = Usage.objects.count()
        print(f"1. 总用量记录数: {total_count}")
        
        # 2. 检查有visitMcc的记录数
        with_visit_mcc = Usage.objects.filter(visitMcc__isnull=False).exclude(visitMcc='').count()
        print(f"2. 有visitMcc的记录数: {with_visit_mcc}")
        
        # 3. 检查有visitMnc的记录数
        with_visit_mnc = Usage.objects.filter(visitMnc__isnull=False).exclude(visitMnc='').count()
        print(f"3. 有visitMnc的记录数: {with_visit_mnc}")
        
        # 4. 检查最新的几条记录
        print("4. 最新的5条记录:")
        recent_usages = Usage.objects.all().order_by('-id')[:5]
        for usage in recent_usages:
            print(f"   ID: {usage.id}, Date: {usage.usageDate}, MCC: '{usage.visitMcc}', MNC: '{usage.visitMnc}'")
        
        # 5. 检查有visitMcc的记录示例
        if with_visit_mcc > 0:
            print("5. 有visitMcc的记录示例:")
            sample_usage = Usage.objects.filter(visitMcc__isnull=False).exclude(visitMcc='').first()
            print(f"   ID: {sample_usage.id}, Date: {sample_usage.usageDate}, MCC: '{sample_usage.visitMcc}', MNC: '{sample_usage.visitMnc}'")
        else:
            print("5. 没有找到有visitMcc的记录")
        
        print("=== 检查完成 ===")
        
    except Exception as e:
        print(f"检查失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_visit_fields()
