"""
文档管理模型
"""
import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Document(models.Model):
    """
    文档模型 - 管理CDR文件处理状态
    """
    # 处理状态选择
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('success', '处理成功'),
        ('failed', '处理失败'),
    ]
    
    # 文件类型选择
    FILE_TYPE_CHOICES = [
        ('data', '数据用量'),
        ('voice', '语音用量'),
        ('smsc', '短信中心'),
        ('used', '已使用'),
        ('imei', '设备识别码'),
        ('locu', '位置更新'),
    ]
    
    # 基础字段
    filename = models.CharField(
        max_length=255,
        verbose_name='文件名'
    )
    
    file_path = models.CharField(
        max_length=500,
        verbose_name='文件路径'
    )
    
    file_size = models.BigIntegerField(
        verbose_name='文件大小(字节)'
    )
    
    # 文件信息解析
    file_prefix = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='文件前缀'
    )
    
    record_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='记录类型'
    )
    
    host_node = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='主机节点'
    )
    
    cdr_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CDR类型'
    )
    
    version = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='版本'
    )
    
    file_date = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name='文件日期'
    )
    
    # 处理状态
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='处理状态'
    )
    
    # 处理统计
    total_iccid_count = models.IntegerField(
        default=0,
        verbose_name='ICCID总数'
    )
    
    processed_iccid_count = models.IntegerField(
        default=0,
        verbose_name='已处理ICCID数'
    )
    
    success_iccid_count = models.IntegerField(
        default=0,
        verbose_name='成功处理ICCID数'
    )
    
    failed_iccid_count = models.IntegerField(
        default=0,
        verbose_name='失败ICCID数'
    )
    
    # 时间字段
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理完成时间'
    )
    
    # 错误信息
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='错误信息'
    )
    
    class Meta:
        db_table = 'document_document'
        verbose_name = '文档'
        verbose_name_plural = '文档管理'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['file_date', 'record_type']),
        ]
    
    def __str__(self):
        return f"{self.filename} - {self.get_status_display()}"
    
    @property
    def progress_percentage(self):
        """处理进度百分比"""
        if self.total_iccid_count == 0:
            return 0
        return round((self.processed_iccid_count / self.total_iccid_count) * 100, 2)
    
    @property
    def success_rate(self):
        """成功率"""
        if self.processed_iccid_count == 0:
            return 0
        return round((self.success_iccid_count / self.processed_iccid_count) * 100, 2)
    
    def mark_as_processing(self):
        """标记为处理中"""
        self.status = 'processing'
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_success(self):
        """标记为处理成功"""
        self.status = 'success'
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'processed_at', 'updated_at'])
    
    def mark_as_failed(self, error_message=None):
        """标记为处理失败"""
        self.status = 'failed'
        self.processed_at = timezone.now()
        if error_message:
            self.error_message = error_message
        self.save(update_fields=['status', 'processed_at', 'error_message', 'updated_at'])


class BadCase(models.Model):
    """
    错误案例模型 - 记录API调用失败的详细信息
    """
    # API类型选择
    API_TYPE_CHOICES = [
        ('user', '用户信息'),
        ('subscription', '订阅信息'),
        ('usage', '用量信息'),
    ]
    
    # 关联文档
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='bad_cases',
        verbose_name='关联文档'
    )
    
    # ICCID信息
    iccid = models.CharField(
        max_length=20,
        verbose_name='ICCID'
    )
    
    # API调用信息
    api_type = models.CharField(
        max_length=20,
        choices=API_TYPE_CHOICES,
        verbose_name='API类型'
    )
    
    trans_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='事务ID'
    )
    
    status_code = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='HTTP状态码'
    )
    
    # 响应数据
    response_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name='完整JSON响应'
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='错误信息'
    )
    
    # 重试信息
    retry_count = models.IntegerField(
        default=0,
        verbose_name='重试次数'
    )
    
    last_retry_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='最后重试时间'
    )
    
    # 时间字段
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'document_badcase'
        verbose_name = '错误案例'
        verbose_name_plural = '错误案例管理'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document', 'api_type']),
            models.Index(fields=['iccid', 'created_at']),
            models.Index(fields=['status_code', 'created_at']),
        ]
        # 唯一约束：同一文档、同一ICCID、同一API类型只能有一条记录
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'iccid', 'api_type'],
                name='unique_badcase_document_iccid_api'
            )
        ]
    
    def __str__(self):
        return f"{self.iccid} - {self.get_api_type_display()} - {self.status_code or 'N/A'}"
    
    def increment_retry(self):
        """增加重试次数"""
        self.retry_count += 1
        self.last_retry_at = timezone.now()
        self.save(update_fields=['retry_count', 'last_retry_at', 'updated_at'])
    
    @property
    def can_retry(self):
        """是否可以重试"""
        return self.retry_count < 2  # 最多重试2次