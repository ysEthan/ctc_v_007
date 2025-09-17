"""
权限管理模块
"""
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    超级管理员权限
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'super_admin'
        )


class IsAdmin(BasePermission):
    """
    管理员权限（包括超级管理员）
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type in ['super_admin', 'admin']
        )


class IsActiveUser(BasePermission):
    """
    激活用户权限
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_active_user
        )


class IsOwnerOrAdmin(BasePermission):
    """
    对象所有者或管理员权限
    """
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问所有对象
        if request.user.is_admin:
            return True
        
        # 用户只能访问自己的对象
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        
        return False


class IsEmailVerified(BasePermission):
    """
    邮箱已验证权限
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.email_verified
        )


class ReadOnlyOrAdmin(BasePermission):
    """
    只读或管理员权限
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_admin


def require_permission(permission_class):
    """
    权限装饰器
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            permission = permission_class()
            if not permission.has_permission(request, None):
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("您没有权限执行此操作")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_super_admin(view_func):
    """
    需要超级管理员权限的装饰器
    """
    return require_permission(IsSuperAdmin)(view_func)


def require_admin(view_func):
    """
    需要管理员权限的装饰器
    """
    return require_permission(IsAdmin)(view_func)


def require_active_user(view_func):
    """
    需要激活用户权限的装饰器
    """
    return require_permission(IsActiveUser)(view_func)


def require_email_verified(view_func):
    """
    需要邮箱验证权限的装饰器
    """
    return require_permission(IsEmailVerified)(view_func)
