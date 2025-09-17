#!/usr/bin/env python
"""
测试用量API的脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from apps.Usage.models import Usage
from apps.Usage.views import UsageListView
from django.http import HttpRequest
from django.contrib.auth import get_user_model

def test_usage_api():
    """测试用量API"""
    try:
        print("=== 测试用量API ===")
        
        # 1. 测试模型查询
        print("1. 测试模型查询...")
        usage_count = Usage.objects.count()
        print(f"   用量记录总数: {usage_count}")
        
        if usage_count > 0:
            first_usage = Usage.objects.first()
            print(f"   第一条记录: ID={first_usage.id}, Date={first_usage.usageDate}, Subscription={first_usage.subscriptionId}")
        
        # 2. 测试视图查询
        print("2. 测试视图查询...")
        User = get_user_model()
        user = User.objects.first()
        
        if user:
            request = HttpRequest()
            request.user = user
            request.method = 'GET'
            
            view = UsageListView()
            view.request = request
            
            queryset = view.get_queryset()
            print(f"   视图查询结果数量: {queryset.count()}")
            
            if queryset.count() > 0:
                first_record = queryset.first()
                print(f"   第一条记录: {first_record}")
        else:
            print("   没有找到用户")
        
        # 3. 测试序列化器
        print("3. 测试序列化器...")
        from apps.Usage.serializers import UsageListSerializer
        
        if usage_count > 0:
            usage = Usage.objects.first()
            serializer = UsageListSerializer(usage)
            print(f"   序列化结果: {serializer.data}")
        
        print("=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_usage_api()
