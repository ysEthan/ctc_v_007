"""
文档管理序列化器
"""
from rest_framework import serializers
from .models import Document, BadCase


class DocumentSerializer(serializers.ModelSerializer):
    """
    文档序列化器
    """
    progress_percentage = serializers.ReadOnlyField()
    success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'filename', 'file_path', 'file_size',
            'file_prefix', 'record_type', 'host_node', 'cdr_type',
            'version', 'file_date', 'status',
            'total_iccid_count', 'processed_iccid_count',
            'success_iccid_count', 'failed_iccid_count',
            'progress_percentage', 'success_rate',
            'created_at', 'updated_at', 'processed_at', 'error_message'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'processed_at',
            'progress_percentage', 'success_rate'
        ]


class DocumentListSerializer(serializers.ModelSerializer):
    """
    文档列表序列化器（简化版）
    """
    progress_percentage = serializers.ReadOnlyField()
    success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'filename', 'file_size', 'record_type',
            'file_date', 'status', 'total_iccid_count',
            'processed_iccid_count', 'success_iccid_count',
            'failed_iccid_count', 'progress_percentage',
            'success_rate', 'created_at', 'processed_at'
        ]


class DocumentCreateSerializer(serializers.ModelSerializer):
    """
    文档创建序列化器
    """
    class Meta:
        model = Document
        fields = [
            'filename', 'file_path', 'file_size',
            'file_prefix', 'record_type', 'host_node',
            'cdr_type', 'version', 'file_date'
        ]


class DocumentUpdateSerializer(serializers.ModelSerializer):
    """
    文档更新序列化器
    """
    class Meta:
        model = Document
        fields = [
            'status', 'total_iccid_count', 'processed_iccid_count',
            'success_iccid_count', 'failed_iccid_count', 'error_message'
        ]


class BadCaseSerializer(serializers.ModelSerializer):
    """
    错误案例序列化器
    """
    can_retry = serializers.ReadOnlyField()
    
    class Meta:
        model = BadCase
        fields = [
            'id', 'document', 'iccid', 'api_type',
            'trans_id', 'status_code', 'response_data',
            'error_message', 'retry_count', 'last_retry_at',
            'can_retry', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'can_retry'
        ]


class BadCaseListSerializer(serializers.ModelSerializer):
    """
    错误案例列表序列化器（简化版）
    """
    can_retry = serializers.ReadOnlyField()
    document_filename = serializers.CharField(source='document.filename', read_only=True)
    
    class Meta:
        model = BadCase
        fields = [
            'id', 'document_filename', 'iccid', 'api_type',
            'status_code', 'error_message', 'retry_count',
            'can_retry', 'created_at'
        ]


class DocumentStatisticsSerializer(serializers.Serializer):
    """
    文档统计序列化器
    """
    total_documents = serializers.IntegerField()
    pending_documents = serializers.IntegerField()
    processing_documents = serializers.IntegerField()
    success_documents = serializers.IntegerField()
    failed_documents = serializers.IntegerField()
    total_iccid_processed = serializers.IntegerField()
    total_iccid_success = serializers.IntegerField()
    total_iccid_failed = serializers.IntegerField()
    success_rate = serializers.FloatField()
    avg_processing_time = serializers.FloatField()


class BadCaseStatisticsSerializer(serializers.Serializer):
    """
    错误案例统计序列化器
    """
    total_bad_cases = serializers.IntegerField()
    user_api_errors = serializers.IntegerField()
    subscription_api_errors = serializers.IntegerField()
    usage_api_errors = serializers.IntegerField()
    retryable_cases = serializers.IntegerField()
    error_by_status_code = serializers.DictField()
