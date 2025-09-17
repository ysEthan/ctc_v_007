"""
订阅视图
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import Subscription
from .serializers import (
    SubscriptionSerializer, SubscriptionListSerializer, 
    SubscriptionCreateSerializer, SubscriptionUpdateSerializer
)
from apps.authentication.permissions import IsAdmin, IsActiveUser


class SubscriptionListView(generics.ListCreateAPIView):
    """
    订阅列表和创建视图
    """
    queryset = Subscription.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'productFlag', 'brand', 'priority']
    search_fields = ['subscriptionId', 'productId', 'brand']
    ordering_fields = ['created_at', 'effTime', 'expTime', 'subscriptionId']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubscriptionCreateSerializer
        return SubscriptionListSerializer
    
    def get_queryset(self):
        queryset = Subscription.objects.all()
        
        # 根据用户权限过滤数据
        user = self.request.user
        if user.user_type == 'user':
            # 普通用户只能看到自己的数据（如果有userId字段关联）
            # 这里可以根据实际业务需求调整
            pass
        
        return queryset


class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    订阅详情、更新和删除视图
    """
    queryset = Subscription.objects.all()
    permission_classes = [IsActiveUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubscriptionUpdateSerializer
        return SubscriptionSerializer
    
    def destroy(self, request, *args, **kwargs):
        """软删除：将status设置为已退订"""
        instance = self.get_object()
        instance.status = '4'  # 退订中
        instance.save()
        return Response({'message': '订阅已标记为退订'}, status=status.HTTP_200_OK)


class SubscriptionSearchView(generics.ListAPIView):
    """
    订阅搜索视图
    """
    serializer_class = SubscriptionListSerializer
    permission_classes = [IsActiveUser]
    
    def get_queryset(self):
        queryset = Subscription.objects.all()
        search_term = self.request.query_params.get('q', None)
        
        if search_term:
            queryset = queryset.filter(
                Q(subscriptionId__icontains=search_term) |
                Q(productId__icontains=search_term) |
                Q(brand__icontains=search_term)
            )
        
        return queryset


@api_view(['GET'])
@permission_classes([IsActiveUser])
def subscription_statistics(request):
    """
    订阅统计信息
    """
    total_count = Subscription.objects.count()
    subscribing_count = Subscription.objects.filter(status='0').count()
    inactive_count = Subscription.objects.filter(status='1').count()
    normal_count = Subscription.objects.filter(status='2').count()
    expired_count = Subscription.objects.filter(status='3').count()
    unsubscribing_count = Subscription.objects.filter(status='4').count()
    locked_count = Subscription.objects.filter(status='5').count()
    
    return Response({
        'total': total_count,
        'subscribing': subscribing_count,
        'inactive': inactive_count,
        'normal': normal_count,
        'expired': expired_count,
        'unsubscribing': unsubscribing_count,
        'locked': locked_count,
    })


@api_view(['POST'])
@permission_classes([IsAdmin])
def subscription_bulk_import(request):
    """
    订阅批量导入
    """
    # 这里可以实现批量导入逻辑
    # 暂时返回成功消息
    return Response({
        'message': '批量导入功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsActiveUser])
def subscription_export(request):
    """
    订阅数据导出
    """
    # 这里可以实现数据导出逻辑
    # 暂时返回成功消息
    return Response({
        'message': '数据导出功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)
