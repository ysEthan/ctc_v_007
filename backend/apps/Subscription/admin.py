"""
订阅管理后台
"""
from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'subscriptionId', 'userId', 'acctId', 'brand', 'productId',
        'status', 'priority', 'effTime', 'expTime', 'created_at'
    ]
    list_filter = [
        'status', 'productFlag', 'brand', 'priority', 'created_at'
    ]
    search_fields = ['subscriptionId', 'productId', 'brand']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('基础信息', {
            'fields': ('subscriptionId', 'userId', 'acctId', 'brand')
        }),
        ('产品信息', {
            'fields': ('productId', 'productFlag', 'priority')
        }),
        ('订阅状态', {
            'fields': ('status', 'statusTime', 'changeReason')
        }),
        ('有效期管理', {
            'fields': ('validityUnit', 'validityTime', 'activeDeadline')
        }),
        ('时间信息', {
            'fields': ('effTime', 'expTime', 'createTime')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
