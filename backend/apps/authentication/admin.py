"""
认证相关管理界面
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, EmailVerification, UserGroup, LoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    用户管理界面
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'user_type', 'status', 'email_verified', 'is_active',
        'last_login', 'created_at'
    ]
    list_filter = [
        'user_type', 'status', 'email_verified', 'is_active',
        'is_staff', 'is_superuser', 'created_at', 'last_login'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')
        }),
        ('权限设置', {
            'fields': ('user_type', 'status', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
        ('登录信息', {
            'fields': ('last_login_ip',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    邮箱验证管理界面
    """
    list_display = [
        'email', 'verification_code', 'is_used', 'is_expired',
        'expires_at', 'created_at'
    ]
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['email', 'verification_code', 'verification_token']
    readonly_fields = ['verification_token', 'created_at']
    ordering = ['-created_at']
    
    def is_expired(self, obj):
        """显示是否过期"""
        if obj.is_expired():
            return format_html('<span style="color: red;">已过期</span>')
        return format_html('<span style="color: green;">有效</span>')
    is_expired.short_description = '是否过期'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    """
    用户组管理界面
    """
    list_display = ['group', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['group__name', 'description']
    filter_horizontal = ['permissions']
    ordering = ['group__name']


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """
    登录日志管理界面
    """
    list_display = [
        'user', 'login_ip', 'is_successful', 'failure_reason',
        'login_time'
    ]
    list_filter = ['is_successful', 'login_time', 'user__user_type']
    search_fields = ['user__username', 'login_ip', 'user_agent']
    readonly_fields = ['login_time']
    ordering = ['-login_time']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False