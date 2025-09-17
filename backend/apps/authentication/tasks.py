"""
认证相关Celery任务
"""
import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task

from .models import User, EmailVerification


@shared_task
def send_verification_email_task(user_id):
    """
    发送邮箱验证邮件任务
    """
    try:
        user = User.objects.get(id=user_id)
        
        # 生成6位数字验证码
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # 创建验证记录
        verification = EmailVerification.objects.create(
            user=user,
            email=user.email,
            verification_code=verification_code,
            expires_at=timezone.now() + timedelta(minutes=30)  # 30分钟过期
        )
        
        # 准备邮件内容
        subject = '邮箱验证 - CTC系统'
        
        # 渲染邮件模板
        context = {
            'user': user,
            'verification_code': verification_code,
            'verification_token': verification.verification_token,
            'expires_at': verification.expires_at,
            'site_name': getattr(settings, 'SITE_NAME', 'CTC系统'),
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3001'),
        }
        
        html_message = render_to_string('emails/verification_email.html', context)
        plain_message = render_to_string('emails/verification_email.txt', context)
        
        # 发送邮件
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f'验证邮件已发送到 {user.email}'
        
    except User.DoesNotExist:
        return f'用户 {user_id} 不存在'
    except Exception as e:
        return f'发送邮件失败: {str(e)}'


@shared_task
def send_welcome_email_task(user_id):
    """
    发送欢迎邮件任务
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = '欢迎注册 - CTC系统'
        
        context = {
            'user': user,
            'site_name': getattr(settings, 'SITE_NAME', 'CTC系统'),
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3001'),
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = render_to_string('emails/welcome_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f'欢迎邮件已发送到 {user.email}'
        
    except User.DoesNotExist:
        return f'用户 {user_id} 不存在'
    except Exception as e:
        return f'发送邮件失败: {str(e)}'


@shared_task
def send_password_reset_email_task(user_id, reset_token):
    """
    发送密码重置邮件任务
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = '密码重置 - CTC系统'
        
        context = {
            'user': user,
            'reset_token': reset_token,
            'site_name': getattr(settings, 'SITE_NAME', 'CTC系统'),
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3001'),
        }
        
        html_message = render_to_string('emails/password_reset_email.html', context)
        plain_message = render_to_string('emails/password_reset_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f'密码重置邮件已发送到 {user.email}'
        
    except User.DoesNotExist:
        return f'用户 {user_id} 不存在'
    except Exception as e:
        return f'发送邮件失败: {str(e)}'


@shared_task
def cleanup_expired_verifications():
    """
    清理过期的验证码任务
    """
    try:
        expired_count = EmailVerification.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        return f'已清理 {expired_count} 个过期验证码'
        
    except Exception as e:
        return f'清理过期验证码失败: {str(e)}'
