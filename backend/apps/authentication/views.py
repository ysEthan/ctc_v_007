"""
认证相关视图
"""
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, EmailVerification, LoginLog
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, EmailVerificationSerializer,
    ResendVerificationSerializer, UserListSerializer, LoginLogSerializer
)
from .permissions import (
    IsSuperAdmin, IsAdmin, IsActiveUser, IsOwnerOrAdmin,
    IsEmailVerified, ReadOnlyOrAdmin
)


class UserRegistrationView(APIView):
    """
    用户注册视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 发送验证邮件
            self._send_verification_email(user)
            
            return Response({
                'message': '注册成功，请查收邮箱验证邮件',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _send_verification_email(self, user):
        """发送验证邮件"""
        from .tasks import send_verification_email_task
        send_verification_email_task.delay(user.id)


class UserLoginView(TokenObtainPairView):
    """
    用户登录视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember_me = serializer.validated_data.get('remember_me', False)
            
            # 记录登录日志
            self._log_login(user, request, True)
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # 设置token过期时间
            if remember_me:
                access_token.set_exp(lifetime=timedelta(days=7))
            
            # 更新用户最后登录信息
            user.last_login_ip = self._get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            })
        
        # 记录登录失败日志
        username_or_email = request.data.get('username_or_email', '')
        failure_reason = self._get_failure_reason(serializer.errors)
        
        try:
            user = User.objects.get_by_username_or_email(username_or_email)
            self._log_login(user, request, False, failure_reason)
        except User.DoesNotExist:
            # 用户不存在时，创建一个临时用户记录用于日志
            self._log_login_failure(username_or_email, request, failure_reason)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_failure_reason(self, errors):
        """从验证错误中提取失败原因"""
        if 'username_or_email' in errors:
            return '用户不存在'
        elif 'password' in errors:
            return '密码错误'
        elif 'non_field_errors' in errors:
            non_field_errors = errors['non_field_errors']
            if any('禁用' in error for error in non_field_errors):
                return '账户已被禁用'
            elif any('验证' in error for error in non_field_errors):
                return '邮箱未验证'
        return '登录失败'
    
    def _log_login_failure(self, username_or_email, request, failure_reason):
        """记录用户不存在的登录失败日志"""
        # 创建一个临时用户对象用于日志记录
        try:
            # 尝试通过邮箱查找
            if '@' in username_or_email:
                user = User.objects.get(email=username_or_email)
            else:
                user = User.objects.get(username=username_or_email)
            self._log_login(user, request, False, failure_reason)
        except User.DoesNotExist:
            # 如果用户真的不存在，记录一个特殊的日志
            LoginLog.objects.create(
                user=None,
                login_ip=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                is_successful=False,
                failure_reason=f'用户不存在: {username_or_email}'
            )
    
    def _log_login(self, user, request, is_successful, failure_reason=''):
        """记录登录日志"""
        LoginLog.objects.create(
            user=user,
            login_ip=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_successful=is_successful,
            failure_reason=failure_reason
        )


class EmailVerificationView(APIView):
    """
    邮箱验证视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            
            # 查找有效的验证码
            verification = EmailVerification.objects.filter(
                verification_code=verification_code,
                is_used=False
            ).first()
            
            if not verification or verification.is_expired():
                return Response({
                    'error': '验证码无效或已过期'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证成功，激活用户
            user = verification.user
            user.email_verified = True
            user.status = 'active'
            user.save(update_fields=['email_verified', 'status'])
            
            # 标记验证码为已使用
            verification.is_used = True
            verification.save(update_fields=['is_used'])
            
            return Response({
                'message': '邮箱验证成功'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    """
    重新发送验证邮件视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # 发送验证邮件
            self._send_verification_email(user)
            
            return Response({
                'message': '验证邮件已重新发送'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _send_verification_email(self, user):
        """发送验证邮件"""
        from .tasks import send_verification_email_task
        send_verification_email_task.delay(user.id)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    用户资料视图
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    用户信息更新视图
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """
    密码修改视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            
            return Response({
                'message': '密码修改成功'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    用户列表视图（管理员）
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_type', 'status', 'email_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'last_login', 'username']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    用户详情视图（管理员）
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        return User.objects.all()


class LoginLogListView(generics.ListAPIView):
    """
    登录日志列表视图（管理员）
    """
    serializer_class = LoginLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_successful', 'user__user_type']
    search_fields = ['user__username', 'login_ip']
    ordering_fields = ['login_time']
    ordering = ['-login_time']
    
    def get_queryset(self):
        return LoginLog.objects.select_related('user')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    用户登出视图
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': '登出成功'})
    except Exception as e:
        return Response({'error': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info_view(request):
    """
    获取当前用户信息
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)