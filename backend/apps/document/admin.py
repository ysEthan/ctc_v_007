"""
文档管理后台
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Document, BadCase


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    文档管理后台
    """
    list_display = [
        'filename', 'record_type', 'file_date', 'status',
        'progress_display', 'success_rate_display',
        'total_iccid_count', 'processed_iccid_count',
        'created_at', 'processed_at'
    ]
    
    list_filter = [
        'status', 'record_type', 'host_node', 'cdr_type',
        'created_at', 'processed_at'
    ]
    
    search_fields = [
        'filename', 'file_prefix', 'host_node', 'file_date'
    ]
    
    readonly_fields = [
        'filename', 'file_path', 'file_size', 'file_prefix',
        'record_type', 'host_node', 'cdr_type', 'version',
        'file_date', 'total_iccid_count', 'processed_iccid_count',
        'success_iccid_count', 'failed_iccid_count',
        'progress_percentage', 'success_rate',
        'created_at', 'updated_at', 'processed_at'
    ]
    
    fieldsets = (
        ('文件信息', {
            'fields': (
                'filename', 'file_path', 'file_size',
                'file_prefix', 'record_type', 'host_node',
                'cdr_type', 'version', 'file_date'
            )
        }),
        ('处理状态', {
            'fields': (
                'status', 'total_iccid_count', 'processed_iccid_count',
                'success_iccid_count', 'failed_iccid_count',
                'progress_percentage', 'success_rate'
            )
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'processed_at')
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-created_at']
    
    def progress_display(self, obj):
        """进度显示"""
        percentage = obj.progress_percentage
        color = 'green' if percentage == 100 else 'orange' if percentage > 0 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, percentage
        )
    progress_display.short_description = '处理进度'
    
    def success_rate_display(self, obj):
        """成功率显示"""
        rate = obj.success_rate
        color = 'green' if rate >= 90 else 'orange' if rate >= 70 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = '成功率'
    
    def has_add_permission(self, request):
        """禁止手动添加文档"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """只有超级管理员可以删除"""
        return request.user.is_superuser


@admin.register(BadCase)
class BadCaseAdmin(admin.ModelAdmin):
    """
    错误案例管理后台
    """
    list_display = [
        'iccid', 'api_type', 'status_code', 'retry_count',
        'can_retry_display', 'document_link', 'created_at'
    ]
    
    list_filter = [
        'api_type', 'status_code', 'retry_count',
        'document__status', 'created_at'
    ]
    
    search_fields = [
        'iccid', 'trans_id', 'error_message',
        'document__filename'
    ]
    
    readonly_fields = [
        'document', 'iccid', 'api_type', 'trans_id',
        'status_code', 'response_data', 'error_message',
        'retry_count', 'last_retry_at', 'can_retry',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'document', 'iccid', 'api_type',
                'trans_id', 'status_code'
            )
        }),
        ('响应数据', {
            'fields': ('response_data',),
            'classes': ('collapse',)
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('重试信息', {
            'fields': ('retry_count', 'last_retry_at', 'can_retry')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    ordering = ['-created_at']
    
    def can_retry_display(self, obj):
        """可重试状态显示"""
        if obj.can_retry:
            return format_html('<span style="color: green;">可重试</span>')
        else:
            return format_html('<span style="color: red;">不可重试</span>')
    can_retry_display.short_description = '重试状态'
    
    def document_link(self, obj):
        """文档链接"""
        url = reverse('admin:document_document_change', args=[obj.document.id])
        return format_html('<a href="{}">{}</a>', url, obj.document.filename)
    document_link.short_description = '关联文档'
    
    def has_add_permission(self, request):
        """禁止手动添加错误案例"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """只有超级管理员可以删除"""
        return request.user.is_superuser
    
    def response_data_display(self, obj):
        """响应数据显示"""
        if obj.response_data:
            import json
            return format_html(
                '<pre style="max-height: 200px; overflow-y: auto;">{}</pre>',
                json.dumps(obj.response_data, indent=2, ensure_ascii=False)
            )
        return '-'
    response_data_display.short_description = '响应数据'