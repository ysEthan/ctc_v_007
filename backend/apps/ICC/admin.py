"""
ICC管理后台
"""
from django.contrib import admin
from .models import ICC


@admin.register(ICC)
class ICCAdmin(admin.ModelAdmin):
    list_display = [
        'iccid', 'imsi', 'msisdn', 'brand', 'lifeCycle', 'paidFlag',
        'activeTime', 'expTime', 'created_at'
    ]
    list_filter = [
        'lifeCycle', 'paidFlag', 'brand', 'hlrState', 'created_at'
    ]
    search_fields = ['iccid', 'imsi', 'msisdn', 'brand']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('基础信息', {
            'fields': ('iccid', 'imsi', 'msisdn', 'brand', 'rateplanId')
        }),
        ('用户信息', {
            'fields': ('userid', 'custid', 'acctid', 'paidFlag')
        }),
        ('生命周期', {
            'fields': ('lifeCycle', 'lifeCycleTime', 'suspendReason', 'activeType')
        }),
        ('有效期管理', {
            'fields': ('validityUnit', 'validityTime', 'activeDeadline')
        }),
        ('时间信息', {
            'fields': ('activeTime', 'effTime', 'expTime', 'createTime')
        }),
        ('设备状态', {
            'fields': ('hlrState',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
