"""
ICC管理模型
"""
from django.db import models
from django.core.validators import RegexValidator


class ICC(models.Model):
    """
    ICC (Integrated Circuit Card) 模型
    """
    # 生命周期状态选择
    LIFECYCLE_CHOICES = [
        ('0', '未激活 (Inactive)'),
        ('1', '活跃 (Active)'),
        ('2', '已停机 (Suspended)'),
        ('3', '已锁定 (Locked)'),
        ('4', '已过期 (Expired)'),
        ('5', '已删除 (Deleted)'),
    ]
    
    # 停机原因选择
    SUSPEND_REASON_CHOICES = [
        ('1', '客户要求，默认选项'),
        ('2', '丢失'),
        ('3', '客户要求并保留电话号码'),
        ('4', '欠费（未付租金）'),
        ('5', '超过用户过期时间'),
        ('6', 'SIM卡与手机分离'),
        ('7', '欠费（未付账单）'),
        ('8', '保留'),
        ('9', '其他'),
    ]
    
    # 有效期单位选择
    VALIDITY_UNIT_CHOICES = [
        ('H', '小时'),
        ('D', '日历日'),
        ('M', '日历月'),
        ('N', '永不过期'),
    ]
    
    # 设备状态选择
    HLR_STATE_CHOICES = [
        ('A', '正常 (Normal)'),
        ('B', '丢失 (Loss)'),
        ('G', '暂停 (Suspend)'),
        ('D', '已删除 (Deleted)'),
        ('I', '预删除 (Pre-delete)'),
    ]
    
    # 付费标志选择
    PAID_FLAG_CHOICES = [
        ('0', '预付费'),
        ('1', '后付费'),
    ]
    
    # 基础字段
    userid = models.BigIntegerField(blank=True, null=True, verbose_name='用户ID')
    custid = models.BigIntegerField(blank=True, null=True, verbose_name='客户ID')
    acctid = models.BigIntegerField(blank=True, null=True, verbose_name='账户ID')
    
    # 付费标志
    paidFlag = models.CharField(
        max_length=1,
        choices=PAID_FLAG_CHOICES,
        blank=True,
        null=True,
        verbose_name='付费标志'
    )
    
    # SIM卡信息
    imsi = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{15}$',
            message='IMSI必须是15位数字'
        )],
        verbose_name='IMSI'
    )
    
    iccid = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{20}$',
            message='ICCID必须是20位数字'
        )],
        verbose_name='ICCID'
    )
    
    msisdn = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{1,15}$',
            message='MSISDN必须是1-15位数字'
        )],
        verbose_name='MSISDN'
    )
    
    brand = models.CharField(max_length=50, blank=True, null=True, verbose_name='品牌')
    rateplanId = models.CharField(max_length=16, blank=True, null=True, verbose_name='费率计划ID')
    
    # 生命周期管理
    lifeCycle = models.CharField(
        max_length=1,
        choices=LIFECYCLE_CHOICES,
        blank=True,
        null=True,
        verbose_name='生命周期状态'
    )
    
    lifeCycleTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='生命周期时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='生命周期时间'
    )
    
    suspendReason = models.CharField(
        max_length=1,
        choices=SUSPEND_REASON_CHOICES,
        blank=True,
        null=True,
        verbose_name='停机原因'
    )
    
    activeType = models.CharField(max_length=1, blank=True, null=True, verbose_name='激活类型')
    
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
    activeTime = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{14}$',
            message='激活时间格式：yyyyMMddHHmmss'
        )],
        verbose_name='激活时间'
    )
    
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
    
    # 设备状态
    hlrState = models.CharField(
        max_length=16,
        choices=HLR_STATE_CHOICES,
        blank=True,
        null=True,
        verbose_name='设备状态'
    )
    
    # 时间戳
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
    
    # Django时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'icc_icc'
        verbose_name = 'ICC'
        verbose_name_plural = 'ICC管理'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.iccid} - {self.get_lifeCycle_display() or 'Unknown'}"
    
    @property
    def is_active(self):
        """是否为活跃状态"""
        return self.lifeCycle == '1'
    
    @property
    def is_suspended(self):
        """是否为停机状态"""
        return self.lifeCycle == '2'
    
    @property
    def is_expired(self):
        """是否为过期状态"""
        return self.lifeCycle == '4'
