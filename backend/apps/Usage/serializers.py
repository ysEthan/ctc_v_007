"""
用量序列化器
"""
from rest_framework import serializers
from .models import Usage


class BaseUsageSerializer(serializers.ModelSerializer):
    """用量序列化器基类"""
    
    def validate_usage(self, value):
        """验证用量值"""
        if value is not None and value < 0:
            raise serializers.ValidationError('用量值不能为负数')
        return value
    
    def validate_usageDate(self, value):
        """验证用量日期格式"""
        if len(value) != 8 or not value.isdigit():
            raise serializers.ValidationError('用量日期必须是8位数字，格式：yyyyMMdd')
        
        try:
            year = int(value[:4])
            month = int(value[4:6])
            day = int(value[6:8])
            if year < 2000 or year > 2100:
                raise serializers.ValidationError('年份必须在2000-2100之间')
            if month < 1 or month > 12:
                raise serializers.ValidationError('月份必须在1-12之间')
            if day < 1 or day > 31:
                raise serializers.ValidationError('日期必须在1-31之间')
                
        except ValueError:
            raise serializers.ValidationError('日期格式无效')
        
        return value
    
    def validate_uniqueness(self, attrs, instance=None):
        """验证唯一性约束"""
        usage_date = attrs.get('usageDate')
        subscription = attrs.get('subscription')
        product_id = attrs.get('productId')
        visit_mnc = attrs.get('visitMnc')
        
        # 检查是否存在相同的记录
        queryset = Usage.objects.filter(
            usageDate=usage_date,
            subscription=subscription,
            productId=product_id,
            visitMnc=visit_mnc
        )
        
        # 如果是更新操作，排除当前记录
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                '该日期、订阅、产品和访问地MNC的组合已存在用量记录'
            )
        
        return attrs


class UsageSerializer(BaseUsageSerializer):
    """
    用量基础序列化器
    """
    usageType_display = serializers.CharField(
        source='get_usageType_display',
        read_only=True
    )
    callType_display = serializers.CharField(
        source='get_callType_display',
        read_only=True
    )
    unit_display = serializers.CharField(
        source='get_unit_display',
        read_only=True
    )
    formatted_usage = serializers.CharField(
        read_only=True
    )
    iccid = serializers.SerializerMethodField()
    
    def get_iccid(self, obj):
        """获取ICCID"""
        try:
            return obj.subscription.icc.iccid if obj.subscription and obj.subscription.icc else None
        except:
            return None
    
    class Meta:
        model = Usage
        fields = [
            'id', 'usageDate', 'iccid', 'productId', 'subscription', 'subscriptionId', 'usageType',
            'usageType_display', 'callType', 'callType_display', 'visitMcc',
            'visitMnc', 'usage', 'unit', 'unit_display', 'formatted_usage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'subscriptionId', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """验证唯一性约束"""
        return self.validate_uniqueness(attrs, self.instance)


class UsageListSerializer(serializers.ModelSerializer):
    """
    用量列表序列化器（简化版）
    """
    usageType_display = serializers.CharField(
        source='get_usageType_display',
        read_only=True
    )
    callType_display = serializers.CharField(
        source='get_callType_display',
        read_only=True
    )
    formatted_usage = serializers.CharField(
        read_only=True
    )
    iccid = serializers.SerializerMethodField()
    
    def get_iccid(self, obj):
        """获取ICCID"""
        try:
            return obj.subscription.icc.iccid if obj.subscription and obj.subscription.icc else None
        except:
            return None
    
    class Meta:
        model = Usage
        fields = [
            'id', 'usageDate', 'iccid', 'productId', 'subscriptionId', 'usageType',
            'usageType_display', 'callType', 'callType_display', 'visitMcc',
            'visitMnc', 'usage', 'unit', 'formatted_usage', 'created_at'
        ]


class UsageCreateSerializer(BaseUsageSerializer):
    """
    用量创建序列化器
    """
    class Meta:
        model = Usage
        fields = [
            'usageDate', 'productId', 'subscription', 'usageType',
            'callType', 'visitMcc', 'visitMnc', 'usage', 'unit'
        ]
    
    def validate(self, attrs):
        """验证唯一性约束"""
        return self.validate_uniqueness(attrs)


class UsageUpdateSerializer(BaseUsageSerializer):
    """
    用量更新序列化器
    """
    class Meta:
        model = Usage
        fields = [
            'usageDate', 'productId', 'subscription', 'usageType',
            'callType', 'visitMcc', 'visitMnc', 'usage', 'unit'
        ]
    
    def validate(self, attrs):
        """验证唯一性约束"""
        return self.validate_uniqueness(attrs, self.instance)


class UsageStatisticsSerializer(serializers.Serializer):
    """
    用量统计序列化器
    """
    date = serializers.CharField()
    data_usage = serializers.IntegerField()
    sms_usage = serializers.IntegerField()
    voice_usage = serializers.IntegerField()
    total_usage = serializers.IntegerField()
