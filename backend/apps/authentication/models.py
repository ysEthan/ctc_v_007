"""
用户认证相关模型
"""
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from .managers import UserManager


class User(AbstractUser):
    """
    扩展用户模型
    """
    # 用户类型选择
    USER_TYPE_CHOICES = [
        ('super_admin', '超级管理员'),
        ('admin', '管理员'),
        ('user', '普通用户'),
    ]
    
    # 用户状态选择
    STATUS_CHOICES = [
        ('active', '激活'),
        ('inactive', '未激活'),
        ('banned', '禁用'),
    ]
    
    # 扩展字段
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='user',
        verbose_name='用户类型'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='inactive',
        verbose_name='用户状态'
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name='邮箱地址'
    )
    
    email_verified = models.BooleanField(
        default=False,
        verbose_name='邮箱已验证'
    )
    
    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^1[3-9]\d{9}$',
            message='请输入正确的手机号码'
        )],
        verbose_name='手机号码'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='头像'
    )
    
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='最后登录IP'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    # 使用自定义管理器
    objects = UserManager()
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_super_admin(self):
        """是否为超级管理员"""
        return self.user_type == 'super_admin'
    
    @property
    def is_admin(self):
        """是否为管理员"""
        return self.user_type in ['super_admin', 'admin']
    
    @property
    def is_active_user(self):
        """是否为激活用户"""
        return self.status == 'active' and self.email_verified


class EmailVerification(models.Model):
    """
    邮箱验证码模型
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verifications',
        verbose_name='用户'
    )
    
    email = models.EmailField(
        verbose_name='邮箱地址'
    )
    
    verification_code = models.CharField(
        max_length=6,
        verbose_name='验证码'
    )
    
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name='验证令牌'
    )
    
    is_used = models.BooleanField(
        default=False,
        verbose_name='是否已使用'
    )
    
    expires_at = models.DateTimeField(
        verbose_name='过期时间'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'auth_email_verification'
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.verification_code}"
    
    def is_expired(self):
        """检查验证码是否过期"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """检查验证码是否有效"""
        return not self.is_used and not self.is_expired()


class UserGroup(models.Model):
    """
    用户组模型（扩展Django Group）
    """
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='user_group',
        verbose_name='Django组'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='组描述'
    )
    
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='user_groups',
        verbose_name='权限'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否激活'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'auth_user_group'
        verbose_name = '用户组'
        verbose_name_plural = '用户组'
        ordering = ['group__name']
    
    def __str__(self):
        return self.group.name


class LoginLog(models.Model):
    """
    登录日志模型
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_logs',
        verbose_name='用户'
    )
    
    login_ip = models.GenericIPAddressField(
        verbose_name='登录IP'
    )
    
    user_agent = models.TextField(
        verbose_name='用户代理'
    )
    
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='登录时间'
    )
    
    is_successful = models.BooleanField(
        default=True,
        verbose_name='是否成功'
    )
    
    failure_reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='失败原因'
    )
    
    class Meta:
        db_table = 'auth_login_log'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"