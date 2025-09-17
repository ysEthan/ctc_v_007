"""
ICC序列化器
"""
from rest_framework import serializers
from .models import ICC


class ICCSerializer(serializers.ModelSerializer):
    """
    ICC基础序列化器
    """
    lifeCycle_display = serializers.CharField(
        source='get_lifeCycle_display',
        read_only=True
    )
    paidFlag_display = serializers.CharField(
        source='get_paidFlag_display',
        read_only=True
    )
    suspendReason_display = serializers.CharField(
        source='get_suspendReason_display',
        read_only=True
    )
    validityUnit_display = serializers.CharField(
        source='get_validityUnit_display',
        read_only=True
    )
    hlrState_display = serializers.CharField(
        source='get_hlrState_display',
        read_only=True
    )
    
    class Meta:
        model = ICC
        fields = [
            'id', 'userid', 'custid', 'acctid', 'paidFlag', 'paidFlag_display',
            'imsi', 'iccid', 'msisdn', 'brand', 'rateplanId', 'lifeCycle',
            'lifeCycle_display', 'lifeCycleTime', 'suspendReason',
            'suspendReason_display', 'activeType', 'validityUnit',
            'validityUnit_display', 'validityTime', 'activeTime',
            'activeDeadline', 'hlrState', 'hlrState_display', 'effTime',
            'expTime', 'createTime', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_iccid(self, value):
        """验证ICCID唯一性"""
        if self.instance and self.instance.iccid == value:
            return value
        
        if ICC.objects.filter(iccid=value).exists():
            raise serializers.ValidationError('ICCID已存在')
        return value
    
    def validate_imsi(self, value):
        """验证IMSI格式"""
        if value and len(value) != 15:
            raise serializers.ValidationError('IMSI必须是15位数字')
        return value
    
    def validate_msisdn(self, value):
        """验证MSISDN格式"""
        if value and not value.isdigit():
            raise serializers.ValidationError('MSISDN必须为数字')
        return value


class ICCListSerializer(serializers.ModelSerializer):
    """
    ICC列表序列化器（简化版）
    """
    lifeCycle_display = serializers.CharField(
        source='get_lifeCycle_display',
        read_only=True
    )
    paidFlag_display = serializers.CharField(
        source='get_paidFlag_display',
        read_only=True
    )
    
    class Meta:
        model = ICC
        fields = [
            'id', 'iccid', 'imsi', 'msisdn', 'brand', 'lifeCycle',
            'lifeCycle_display', 'paidFlag', 'paidFlag_display',
            'activeTime', 'expTime', 'created_at'
        ]


class ICCCreateSerializer(serializers.ModelSerializer):
    """
    ICC创建序列化器
    """
    class Meta:
        model = ICC
        fields = [
            'userid', 'custid', 'acctid', 'paidFlag', 'imsi', 'iccid',
            'msisdn', 'brand', 'rateplanId', 'lifeCycle', 'lifeCycleTime',
            'suspendReason', 'activeType', 'validityUnit', 'validityTime',
            'activeTime', 'activeDeadline', 'hlrState', 'effTime',
            'expTime', 'createTime'
        ]
    
    def validate_iccid(self, value):
        """验证ICCID唯一性"""
        if ICC.objects.filter(iccid=value).exists():
            raise serializers.ValidationError('ICCID已存在')
        return value


class ICCUpdateSerializer(serializers.ModelSerializer):
    """
    ICC更新序列化器
    """
    class Meta:
        model = ICC
        fields = [
            'userid', 'custid', 'acctid', 'paidFlag', 'imsi', 'msisdn',
            'brand', 'rateplanId', 'lifeCycle', 'lifeCycleTime',
            'suspendReason', 'activeType', 'validityUnit', 'validityTime',
            'activeTime', 'activeDeadline', 'hlrState', 'effTime',
            'expTime', 'createTime'
        ]
        # ICCID不允许更新
        read_only_fields = ['iccid']
