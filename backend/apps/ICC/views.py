"""
ICC视图
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import ICC
from .serializers import (
    ICCSerializer, ICCListSerializer, ICCCreateSerializer, ICCUpdateSerializer
)
from apps.authentication.permissions import IsAdmin, IsActiveUser


class ICCListView(generics.ListCreateAPIView):
    """
    ICC列表和创建视图
    """
    queryset = ICC.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lifeCycle', 'paidFlag', 'brand', 'hlrState']
    search_fields = ['iccid', 'imsi', 'msisdn', 'brand']
    ordering_fields = ['created_at', 'activeTime', 'expTime', 'iccid']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ICCCreateSerializer
        return ICCListSerializer
    
    def get_queryset(self):
        queryset = ICC.objects.all()
        
        # 根据用户权限过滤数据
        user = self.request.user
        if user.user_type == 'user':
            # 普通用户只能看到自己的数据（如果有userid字段关联）
            # 这里可以根据实际业务需求调整
            pass
        
        return queryset


class ICCDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ICC详情、更新和删除视图
    """
    queryset = ICC.objects.all()
    permission_classes = [IsActiveUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ICCUpdateSerializer
        return ICCSerializer
    
    def destroy(self, request, *args, **kwargs):
        """软删除：将lifeCycle设置为已删除"""
        instance = self.get_object()
        instance.lifeCycle = '5'  # 已删除
        instance.save()
        return Response({'message': 'ICC已标记为删除'}, status=status.HTTP_200_OK)


class ICCSearchView(generics.ListAPIView):
    """
    ICC搜索视图
    """
    serializer_class = ICCListSerializer
    permission_classes = [IsActiveUser]
    
    def get_queryset(self):
        queryset = ICC.objects.all()
        search_term = self.request.query_params.get('q', None)
        
        if search_term:
            queryset = queryset.filter(
                Q(iccid__icontains=search_term) |
                Q(imsi__icontains=search_term) |
                Q(msisdn__icontains=search_term) |
                Q(brand__icontains=search_term)
            )
        
        return queryset


@api_view(['GET'])
@permission_classes([IsActiveUser])
def icc_statistics(request):
    """
    ICC统计信息
    """
    total_count = ICC.objects.count()
    active_count = ICC.objects.filter(lifeCycle='1').count()
    inactive_count = ICC.objects.filter(lifeCycle='0').count()
    suspended_count = ICC.objects.filter(lifeCycle='2').count()
    expired_count = ICC.objects.filter(lifeCycle='4').count()
    deleted_count = ICC.objects.filter(lifeCycle='5').count()
    
    return Response({
        'total': total_count,
        'active': active_count,
        'inactive': inactive_count,
        'suspended': suspended_count,
        'expired': expired_count,
        'deleted': deleted_count,
    })


@api_view(['POST'])
@permission_classes([IsAdmin])
def icc_bulk_import(request):
    """
    ICC批量导入
    """
    # 这里可以实现批量导入逻辑
    # 暂时返回成功消息
    return Response({
        'message': '批量导入功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsActiveUser])
def icc_export(request):
    """
    ICC数据导出
    """
    # 这里可以实现数据导出逻辑
    # 暂时返回成功消息
    return Response({
        'message': '数据导出功能待实现',
        'success': True
    }, status=status.HTTP_200_OK)
