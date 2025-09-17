"""
用户管理器
"""
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    自定义用户管理器
    """
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        创建普通用户
        """
        if not username:
            raise ValueError('用户名不能为空')
        if not email:
            raise ValueError('邮箱不能为空')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        创建超级管理员
        """
        extra_fields.setdefault('user_type', 'super_admin')
        extra_fields.setdefault('status', 'active')
        extra_fields.setdefault('email_verified', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('user_type') != 'super_admin':
            raise ValueError('超级管理员必须是super_admin类型')
        
        return self.create_user(username, email, password, **extra_fields)
    
    def create_admin(self, username, email, password=None, **extra_fields):
        """
        创建管理员
        """
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('status', 'active')
        extra_fields.setdefault('email_verified', True)
        extra_fields.setdefault('is_staff', True)
        
        return self.create_user(username, email, password, **extra_fields)
    
    def get_active_users(self):
        """
        获取激活用户
        """
        return self.filter(status='active', email_verified=True)
    
    def get_by_email(self, email):
        """
        通过邮箱获取用户
        """
        return self.get(email=email)
    
    def get_by_username_or_email(self, username_or_email):
        """
        通过用户名或邮箱获取用户
        """
        try:
            # 先尝试通过用户名查找
            return self.get(username=username_or_email)
        except self.model.DoesNotExist:
            # 再尝试通过邮箱查找
            return self.get(email=username_or_email)
