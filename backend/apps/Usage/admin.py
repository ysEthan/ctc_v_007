"""
用量管理后台
"""
from django.contrib import admin
from .models import Usage


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = [
        'usageDate', 'productId', 'subscriptionId', 'usageType',
        'callType', 'usage', 'unit', 'visitMcc', 'visitMnc', 'created_at'
    ]
    list_filter = [
        'usageType', 'callType', 'unit', 'usageDate', 'created_at'
    ]
    search_fields = ['productId', 'subscriptionId', 'visitMcc', 'visitMnc']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-usageDate', '-created_at']
    
    fieldsets = (
        ('基础信息', {
            'fields': ('usageDate', 'productId', 'subscriptionId')
        }),
        ('用量信息', {
            'fields': ('usageType', 'callType', 'usage', 'unit')
        }),
        ('访问地信息', {
            'fields': ('visitMcc', 'visitMnc')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
