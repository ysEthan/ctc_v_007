"""
用量管理模型
"""
from django.db import models
from django.core.validators import RegexValidator


class Usage(models.Model):
    """
    用量模型
    """
    # 用量类型选择
    USAGE_TYPE_CHOICES = [
        ('dat', '数据'),
        ('sms', '短信'),
        ('voc', '语音'),
    ]
    
    # 呼叫类型选择
    CALL_TYPE_CHOICES = [
        ('0', '主叫 (MO)'),
        ('1', '被叫 (MT)'),
        ('*', '全部 (ALL)'),
    ]
    
    # 用量单位选择
    UNIT_CHOICES = [
        ('Byte', '字节'),
        ('Minute', '分钟'),
        ('String', '条'),
    ]
    
    # 基础字段
    usageDate = models.CharField(
        max_length=8,
        validators=[RegexValidator(
            regex=r'^\d{8}$',
            message='用量日期格式：yyyyMMdd'
        )],
        verbose_name='用量日期'
    )
    
    productId = models.CharField(max_length=16, blank=True, null=True, verbose_name='产品ID')
    
    # 订阅外键关联
    subscription = models.ForeignKey(
        'Subscription.Subscription',
        on_delete=models.CASCADE,
        related_name='usages',
        verbose_name='订阅'
    )
    
    # 保留subscriptionId字段用于兼容性和查询优化（从外键自动填充）
    subscriptionId = models.CharField(max_length=64, blank=True, null=True, verbose_name='订阅ID')
    
    # 用量信息
    usageType = models.CharField(
        max_length=10,
        choices=USAGE_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='用量类型'
    )
    
    callType = models.CharField(
        max_length=1,
        choices=CALL_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='呼叫类型'
    )
    
    # 访问地信息
    visitMcc = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{3}$',
            message='访问地MCC必须是3位数字'
        )],
        verbose_name='访问地MCC'
    )
    
    visitMnc = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{1,6}$',
            message='访问地MNC必须是1-6位数字'
        )],
        verbose_name='访问地MNC'
    )
    
    # 用量数据
    usage = models.BigIntegerField(blank=True, null=True, verbose_name='用量值')
    
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        blank=True,
        null=True,
        verbose_name='用量单位'
    )
    
    # Django时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'usage_usage'
        verbose_name = '用量'
        verbose_name_plural = '用量管理'
        ordering = ['-usageDate', '-created_at']
        # 添加复合索引以提高查询性能
        indexes = [
            models.Index(fields=['usageDate', 'subscriptionId']),
            models.Index(fields=['usageDate', 'productId']),
            models.Index(fields=['usageType', 'usageDate']),
        ]
        # 添加唯一性约束：同一天、同一订阅、同一产品、同一个visitMnc只允许存在一条记录
        constraints = [
            models.UniqueConstraint(
                fields=['usageDate', 'subscription', 'productId', 'visitMnc'],
                name='unique_usage_per_day_subscription_product_mnc'
            )
        ]
    
    def save(self, *args, **kwargs):
        """保存时自动填充subscriptionId"""
        if self.subscription:
            self.subscriptionId = self.subscription.subscriptionId
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.usageDate} - {self.get_usageType_display() or 'Unknown'} - {self.usage or 0}"
    
    @property
    def formatted_usage(self):
        """格式化用量显示 - 统一使用MB"""
        if not self.usage:
            return "0 MB"
        
        if self.unit == 'Byte':
            # 字节转换为MB
            mb_value = self.usage / (1024 * 1024)
            return f"{mb_value:.2f} MB"
        elif self.unit == 'Minute':
            # 分钟转换为MB (假设1分钟语音约等于1MB)
            return f"{self.usage:.2f} MB"
        elif self.unit == 'String':
            # 短信转换为MB (假设1条短信约等于0.001MB)
            mb_value = self.usage * 0.001
            return f"{mb_value:.2f} MB"
        else:
            # 其他单位直接显示数值加MB
            return f"{self.usage:.2f} MB"
    
    @property
    def is_data_usage(self):
        """是否为数据用量"""
        return self.usageType == 'dat'
    
    @property
    def is_sms_usage(self):
        """是否为短信用量"""
        return self.usageType == 'sms'
    
    @property
    def is_voice_usage(self):
        """是否为语音用量"""
        return self.usageType == 'voc'
