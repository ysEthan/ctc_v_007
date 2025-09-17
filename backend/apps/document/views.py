"""
文档管理视图
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count, Avg, Sum
from django.db import models
from django.utils import timezone
from datetime import timedelta

from .models import Document, BadCase
from .serializers import (
    DocumentSerializer, DocumentListSerializer, DocumentCreateSerializer,
    DocumentUpdateSerializer, BadCaseSerializer, BadCaseListSerializer,
    DocumentStatisticsSerializer, BadCaseStatisticsSerializer
)
from apps.authentication.permissions import IsAdmin, IsActiveUser


class DocumentListView(generics.ListCreateAPIView):
    """
    文档列表和创建视图
    """
    queryset = Document.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'record_type', 'file_date', 'host_node']
    search_fields = ['filename', 'file_prefix', 'host_node']
    ordering_fields = ['created_at', 'processed_at', 'file_size', 'filename']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentCreateSerializer
        return DocumentListSerializer
    
    def get_queryset(self):
        queryset = Document.objects.all()
        
        # 根据用户权限过滤数据
        user = self.request.user
        if user.user_type == 'user':
            # 普通用户只能看到自己的数据（如果有相关字段关联）
            # 这里可以根据实际业务需求调整
            pass
        
        return queryset


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    文档详情、更新和删除视图
    """
    queryset = Document.objects.all()
    permission_classes = [IsActiveUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DocumentUpdateSerializer
        return DocumentSerializer


class DocumentSearchView(generics.ListAPIView):
    """
    文档搜索视图
    """
    serializer_class = DocumentListSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'record_type', 'file_date']
    search_fields = ['filename', 'file_prefix', 'host_node']
    ordering_fields = ['created_at', 'processed_at', 'file_size']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Document.objects.all()
        
        # 高级搜索条件
        status_filter = self.request.query_params.get('status')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if date_from:
            queryset = queryset.filter(file_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(file_date__lte=date_to)
        
        return queryset


class BadCaseListView(generics.ListAPIView):
    """
    错误案例列表视图
    """
    queryset = BadCase.objects.all()
    serializer_class = BadCaseListSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['api_type', 'status_code', 'retry_count']
    search_fields = ['iccid', 'error_message']
    ordering_fields = ['created_at', 'retry_count', 'status_code']
    ordering = ['-created_at']


class BadCaseDetailView(generics.RetrieveAPIView):
    """
    错误案例详情视图
    """
    queryset = BadCase.objects.all()
    serializer_class = BadCaseSerializer
    permission_classes = [IsActiveUser]


@api_view(['GET'])
@permission_classes([IsActiveUser])
def document_statistics(request):
    """
    文档统计信息
    """
    # 基础统计
    total_documents = Document.objects.count()
    pending_documents = Document.objects.filter(status='pending').count()
    processing_documents = Document.objects.filter(status='processing').count()
    success_documents = Document.objects.filter(status='success').count()
    failed_documents = Document.objects.filter(status='failed').count()
    
    # ICCID统计
    total_iccid_processed = Document.objects.aggregate(
        total=models.Sum('processed_iccid_count')
    )['total'] or 0
    
    total_iccid_success = Document.objects.aggregate(
        total=models.Sum('success_iccid_count')
    )['total'] or 0
    
    total_iccid_failed = Document.objects.aggregate(
        total=models.Sum('failed_iccid_count')
    )['total'] or 0
    
    # 成功率计算
    success_rate = 0
    if total_iccid_processed > 0:
        success_rate = round((total_iccid_success / total_iccid_processed) * 100, 2)
    
    # 平均处理时间
    avg_processing_time = 0
    completed_documents = Document.objects.filter(
        status__in=['success', 'failed'],
        processed_at__isnull=False
    )
    
    if completed_documents.exists():
        processing_times = []
        for doc in completed_documents:
            if doc.processed_at:
                processing_time = (doc.processed_at - doc.created_at).total_seconds()
                processing_times.append(processing_time)
        
        if processing_times:
            avg_processing_time = round(sum(processing_times) / len(processing_times), 2)
    
    statistics = {
        'total_documents': total_documents,
        'pending_documents': pending_documents,
        'processing_documents': processing_documents,
        'success_documents': success_documents,
        'failed_documents': failed_documents,
        'total_iccid_processed': total_iccid_processed,
        'total_iccid_success': total_iccid_success,
        'total_iccid_failed': total_iccid_failed,
        'success_rate': success_rate,
        'avg_processing_time': avg_processing_time
    }
    
    serializer = DocumentStatisticsSerializer(statistics)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsActiveUser])
def badcase_statistics(request):
    """
    错误案例统计信息
    """
    # 基础统计
    total_bad_cases = BadCase.objects.count()
    user_api_errors = BadCase.objects.filter(api_type='user').count()
    subscription_api_errors = BadCase.objects.filter(api_type='subscription').count()
    usage_api_errors = BadCase.objects.filter(api_type='usage').count()
    
    # 可重试案例
    retryable_cases = BadCase.objects.filter(retry_count__lt=2).count()
    
    # 按状态码统计
    error_by_status_code = {}
    status_codes = BadCase.objects.values('status_code').annotate(
        count=Count('id')
    ).order_by('status_code')
    
    for item in status_codes:
        status_code = item['status_code'] or 'Unknown'
        error_by_status_code[str(status_code)] = item['count']
    
    statistics = {
        'total_bad_cases': total_bad_cases,
        'user_api_errors': user_api_errors,
        'subscription_api_errors': subscription_api_errors,
        'usage_api_errors': usage_api_errors,
        'retryable_cases': retryable_cases,
        'error_by_status_code': error_by_status_code
    }
    
    serializer = BadCaseStatisticsSerializer(statistics)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdmin])
def retry_failed_document(request, document_id):
    """
    重试失败文档处理
    """
    try:
        document = Document.objects.get(id=document_id)
        
        if document.status not in ['failed']:
            return Response(
                {'error': '只能重试失败的文档'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 重置文档状态
        document.status = 'pending'
        document.error_message = None
        document.processed_at = None
        document.save()
        
        # 这里可以触发异步任务重新处理文档
        # from .tasks import process_document_task
        # process_document_task.delay(document.id)
        
        return Response({'message': '文档已加入重试队列'})
        
    except Document.DoesNotExist:
        return Response(
            {'error': '文档不存在'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAdmin])
def retry_badcase(request, badcase_id):
    """
    重试错误案例
    """
    try:
        badcase = BadCase.objects.get(id=badcase_id)
        
        if not badcase.can_retry:
            return Response(
                {'error': '该错误案例已达到最大重试次数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 增加重试次数
        badcase.increment_retry()
        
        # 这里可以触发异步任务重新处理该ICCID
        # from .tasks import process_iccid_task
        # process_iccid_task.delay(badcase.document.id, badcase.iccid, badcase.api_type)
        
        return Response({'message': '错误案例已加入重试队列'})
        
    except BadCase.DoesNotExist:
        return Response(
            {'error': '错误案例不存在'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsActiveUser])
def scan_new_documents(request):
    """
    扫描新文档
    """
    try:
        from tasks.document_scan import scan_and_process_documents as scan_task
        
        # 触发异步扫描任务
        task = scan_task.delay()
        
        return Response({
            'message': '扫描任务已启动',
            'task_id': task.id
        })
        
    except Exception as e:
        logger.error(f"启动扫描任务失败: {str(e)}")
        return Response(
            {'error': f'启动扫描任务失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )