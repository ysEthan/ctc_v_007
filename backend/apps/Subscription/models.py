"""
订阅管理模型
"""
from django.db import models
from django.core.validators import RegexValidator


class Subscription(models.Model):
    """
    订阅模型
    """
    # 产品标志选择
    PRODUCT_FLAG_CHOICES = [
        ('0', '基础套餐'),
        ('1', '附加包'),
    ]
    
    # 订阅状态选择
    STATUS_CHOICES = [
        ('0', '订阅中'),
        ('1', '未激活'),
        ('2', '正常'),
        ('3', '已过期'),
        ('4', '退订中'),
        ('5', '已锁定'),
    ]
    
    # 有效期单位选择
    VALIDITY_UNIT_CHOICES = [
        ('H', '小时'),
        ('D', '日历日'),
        ('M', '日历月'),
        ('N', '永不过期'),
    ]
    
    # 订阅变更原因选择
    CHANGE_REASON_CHOICES = [
        ('1', '使用中'),
        ('2', '速度受限'),
        ('3', '已用尽'),
        ('4', '未激活，已过期'),
        ('5', '未激活，已退订'),
        ('6', '已激活，已过期'),
        ('7', '已激活，已退订'),
    ]
    
    # 产品优先级选择
    PRIORITY_CHOICES = [
        ('20', '最高'),
        ('30', '高'),
        ('40', '中'),
        ('50', '低'),
        ('80', '最低'),
    ]
    
    # 基础字段
    subscriptionId = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='订阅ID'
    )
    
    # ICC外键关联
    icc = models.ForeignKey(
        'ICC.ICC',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='ICC卡'
    )
    
    userId = models.BigIntegerField(blank=True, null=True, verbose_name='用户ID')
    acctId = models.BigIntegerField(blank=True, null=True, verbose_name='账户ID')
    brand = models.CharField(max_length=50, blank=True, null=True, verbose_name='品牌')
    
    # 产品信息
    productId = models.CharField(max_length=16, blank=True, null=True, verbose_name='产品ID')
    productFlag = models.CharField(
        max_length=1,
        choices=PRODUCT_FLAG_CHOICES,
        blank=True,
        null=True,
        verbose_name='产品标志'
    )
    
    # 订阅状态
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='订阅状态'
    )
    
    statusTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='状态时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='状态时间'
    )
    
    # 激活管理
    activeDeadline = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{8}$',
            message='最后激活时间格式：yyyyMMdd'
        )],
        verbose_name='最后激活时间'
    )
    
    # 有效期管理
    validityUnit = models.CharField(
        max_length=1,
        choices=VALIDITY_UNIT_CHOICES,
        blank=True,
        null=True,
        verbose_name='有效期单位'
    )
    
    validityTime = models.IntegerField(blank=True, null=True, verbose_name='有效期时长')
    
    # 时间字段
    effTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='生效时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='生效时间'
    )
    
    expTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='过期时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='过期时间'
    )
    
    createTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='创建时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='创建时间'
    )
    
    # 优先级和变更原因
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        blank=True,
        null=True,
        verbose_name='产品优先级'
    )
    
    changeReason = models.CharField(
        max_length=1,
        choices=CHANGE_REASON_CHOICES,
        blank=True,
        null=True,
        verbose_name='订阅变更原因'
    )
    
    # Django时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'subscription_subscription'
        verbose_name = '订阅'
        verbose_name_plural = '订阅管理'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subscriptionId} - {self.get_status_display() or 'Unknown'}"
    
    @property
    def is_active(self):
        """是否为正常状态"""
        return self.status == '2'
    
    @property
    def is_expired(self):
        """是否为过期状态"""
        return self.status == '3'
    
    @property
    def is_subscribing(self):
        """是否为订阅中状态"""
        return self.status == '0'
