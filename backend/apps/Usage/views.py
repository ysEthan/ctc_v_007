"""
用量视图
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import django_filters

from .models import Usage
from .serializers import (
    UsageSerializer, UsageListSerializer, UsageCreateSerializer,
    UsageUpdateSerializer, UsageStatisticsSerializer
)
from apps.authentication.permissions import IsAdmin, IsActiveUser


class UsageFilter(django_filters.FilterSet):
    """用量过滤器"""
    iccid = django_filters.CharFilter(method='filter_iccid')
    date = django_filters.CharFilter(field_name='usageDate', lookup_expr='icontains')
    mccMnc = django_filters.CharFilter(field_name='visitMnc', lookup_expr='icontains')
    
    def filter_iccid(self, queryset, name, value):
        """通过ICCID过滤"""
        if value:
            return queryset.filter(
                Q(subscription__icc__iccid__icontains=value)
            )
        return queryset
    
    class Meta:
        model = Usage
        fields = ['usageType', 'callType', 'productId', 'subscriptionId', 'usageDate', 'visitMnc']


class UsageListView(generics.ListCreateAPIView):
    """
    用量列表和创建视图
    """
    queryset = Usage.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UsageFilter
    search_fields = ['productId', 'subscriptionId', 'visitMcc', 'visitMnc']
    ordering_fields = ['usageDate', 'usage', 'created_at']
    ordering = ['-usageDate', '-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UsageCreateSerializer
        return UsageListSerializer
    
    def get_queryset(self):
        queryset = Usage.objects.select_related('subscription__icc').all()
        
        # 根据用户权限过滤数据
        user = self.request.user
        if user.user_type == 'user':
            # 普通用户只能看到自己的数据
            # 这里可以根据实际业务需求调整
            pass
        
        return queryset


class UsageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    用量详情、更新和删除视图
    """
    queryset = Usage.objects.select_related('subscription__icc').all()
    permission_classes = [IsActiveUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UsageUpdateSerializer
        return UsageSerializer


class UsageSearchView(generics.ListAPIView):
    """
    用量搜索视图
    """
    serializer_class = UsageListSerializer
    permission_classes = [IsActiveUser]
    
    def get_queryset(self):
        queryset = Usage.objects.select_related('subscription__icc').all()
        search_term = self.request.query_params.get('q', None)
        
        if search_term:
            queryset = queryset.filter(
                Q(productId__icontains=search_term) |
                Q(subscriptionId__icontains=search_term) |
                Q(visitMcc__icontains=search_term) |
                Q(visitMnc__icontains=search_term)
            )
        
        return queryset


@api_view(['GET'])
@permission_classes([IsActiveUser])
def usage_statistics(request):
    """
    用量统计信息
    """
    # 获取查询参数
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    subscription_id = request.query_params.get('subscription_id')
    product_id = request.query_params.get('product_id')
    
    # 构建查询条件
    queryset = Usage.objects.all()
    
    if start_date:
        queryset = queryset.filter(usageDate__gte=start_date)
    if end_date:
        queryset = queryset.filter(usageDate__lte=end_date)
    if subscription_id:
        queryset = queryset.filter(subscriptionId=subscription_id)
    if product_id:
        queryset = queryset.filter(productId=product_id)
    
    # 统计各类型用量
    data_usage = queryset.filter(usageType='dat').aggregate(
        total=Sum('usage')
    )['total'] or 0
    
    sms_usage = queryset.filter(usageType='sms').aggregate(
        total=Sum('usage')
    )['total'] or 0
    
    voice_usage = queryset.filter(usageType='voc').aggregate(
        total=Sum('usage')
    )['total'] or 0
    
    total_records = queryset.count()
    
    return Response({
        'data_usage': data_usage,
        'sms_usage': sms_usage,
        'voice_usage': voice_usage,
        'total_records': total_records,
        'period': {
            'start_date': start_date,
            'end_date': end_date
        }
    })


@api_view(['GET'])
@permission_classes([IsActiveUser])
def usage_daily_statistics(request):
    """
    每日用量统计
    """
    # 获取查询参数
    days = int(request.query_params.get('days', 7))  # 默认7天
    subscription_id = request.query_params.get('subscription_id')
    product_id = request.query_params.get('product_id')
    
    # 计算日期范围
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    # 构建查询条件
    queryset = Usage.objects.filter(
        usageDate__gte=start_date.strftime('%Y%m%d'),
        usageDate__lte=end_date.strftime('%Y%m%d')
    )
    
    if subscription_id:
        queryset = queryset.filter(subscriptionId=subscription_id)
    if product_id:
        queryset = queryset.filter(productId=product_id)
    
    # 按日期分组统计
    daily_stats = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime('%Y%m%d')
        
        day_usage = queryset.filter(usageDate=date_str)
        
        data_usage = day_usage.filter(usageType='dat').aggregate(
            total=Sum('usage')
        )['total'] or 0
        
        sms_usage = day_usage.filter(usageType='sms').aggregate(
            total=Sum('usage')
        )['total'] or 0
        
        voice_usage = day_usage.filter(usageType='voc').aggregate(
            total=Sum('usage')
        )['total'] or 0
        
        daily_stats.append({
            'date': date_str,
            'data_usage': data_usage,
            'sms_usage': sms_usage,
            'voice_usage': voice_usage,
            'total_usage': data_usage + sms_usage + voice_usage
        })
    
    return Response(daily_stats)


@api_view(['POST'])
@permission_classes([IsAdmin])
def usage_bulk_import(request):
    """
    用量批量导入
    """
    # 这里可以实现批量导入逻辑
    # 暂时返回成功消息
    return Response({
        'message': '批量导入功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsActiveUser])
def usage_export(request):
    """
    用量数据导出
    """
    # 这里可以实现数据导出逻辑
    # 暂时返回成功消息
    return Response({
        'message': '数据导出功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)
