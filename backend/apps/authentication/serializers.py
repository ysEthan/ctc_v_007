"""
认证相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, EmailVerification, LoginLog


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        help_text='密码长度至少8位'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text='确认密码'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        ]
        extra_kwargs = {
            'username': {'help_text': '用户名，3-20个字符'},
            'email': {'help_text': '邮箱地址，用于验证和登录'},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
        }
    
    def validate_username(self, value):
        """验证用户名"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value
    
    def validate_email(self, value):
        """验证邮箱"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('邮箱已被注册')
        return value
    
    def validate_password(self, value):
        """验证密码强度"""
        # 自定义密码验证规则
        if len(value) < 8:
            raise serializers.ValidationError('密码长度至少8位')
        
        if not any(c.isalpha() for c in value):
            raise serializers.ValidationError('密码必须包含字母')
        
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError('密码必须包含数字')
        
        return value
    
    def validate(self, attrs):
        """验证密码确认"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username_or_email = serializers.CharField(
        help_text='用户名或邮箱',
        allow_blank=False,
        error_messages={
            'blank': '用户名或邮箱不能为空',
            'required': '用户名或邮箱不能为空'
        }
    )
    password = serializers.CharField(
        write_only=True,
        help_text='密码',
        allow_blank=False,
        error_messages={
            'blank': '密码不能为空',
            'required': '密码不能为空'
        }
    )
    remember_me = serializers.BooleanField(
        default=False,
        help_text='记住登录状态'
    )
    
    def validate(self, attrs):
        """验证登录信息"""
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')
        
        # 尝试通过用户名或邮箱查找用户
        try:
            user = User.objects.get_by_username_or_email(username_or_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'username_or_email': ['用户不存在，请检查用户名或邮箱是否正确']
            })
        
        # 检查用户状态
        if not user.is_active:
            raise serializers.ValidationError({
                'non_field_errors': ['账户已被禁用，请联系管理员']
            })
        
        # 验证密码
        authenticated_user = authenticate(
            username=user.username,
            password=password
        )
        
        if not authenticated_user:
            raise serializers.ValidationError({
                'password': ['密码错误，请重新输入']
            })
        
        # 检查邮箱验证状态
        if not user.email_verified:
            raise serializers.ValidationError({
                'non_field_errors': ['邮箱未验证，请先验证邮箱后再登录']
            })
        
        attrs['user'] = authenticated_user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    """
    user_type_display = serializers.CharField(
        source='get_user_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'avatar', 'user_type', 'user_type_display',
            'status', 'status_display', 'email_verified',
            'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'username', 'user_type', 'status',
            'email_verified', 'last_login', 'created_at', 'updated_at'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户信息更新序列化器
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar']
    
    def validate_phone(self, value):
        """验证手机号"""
        if value and User.objects.filter(phone=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('手机号已被使用')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    """
    old_password = serializers.CharField(
        write_only=True,
        help_text='原密码'
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        help_text='新密码'
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        help_text='确认新密码'
    )
    
    def validate_old_password(self, value):
        """验证原密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
    
    def validate_new_password(self, value):
        """验证新密码强度"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        """验证新密码确认"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('两次输入的新密码不一致')
        return attrs


class EmailVerificationSerializer(serializers.ModelSerializer):
    """
    邮箱验证序列化器
    """
    class Meta:
        model = EmailVerification
        fields = ['verification_code']
    
    def validate_verification_code(self, value):
        """验证验证码格式"""
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('验证码必须是6位数字')
        return value


class ResendVerificationSerializer(serializers.Serializer):
    """
    重新发送验证邮件序列化器
    """
    email = serializers.EmailField(
        help_text='邮箱地址'
    )
    
    def validate_email(self, value):
        """验证邮箱"""
        try:
            user = User.objects.get(email=value)
            if user.email_verified:
                raise serializers.ValidationError('邮箱已验证，无需重新发送')
        except User.DoesNotExist:
            raise serializers.ValidationError('邮箱未注册')
        return value


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化器（管理员使用）
    """
    user_type_display = serializers.CharField(
        source='get_user_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'user_type_display', 'status', 'status_display',
            'email_verified', 'last_login', 'created_at'
        ]


class LoginLogSerializer(serializers.ModelSerializer):
    """
    登录日志序列化器
    """
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    
    class Meta:
        model = LoginLog
        fields = [
            'id', 'username', 'login_ip', 'user_agent',
            'login_time', 'is_successful', 'failure_reason'
        ]
