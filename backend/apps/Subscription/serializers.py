"""
订阅序列化器
"""
from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    订阅基础序列化器
    """
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    productFlag_display = serializers.CharField(
        source='get_productFlag_display',
        read_only=True
    )
    validityUnit_display = serializers.CharField(
        source='get_validityUnit_display',
        read_only=True
    )
    priority_display = serializers.CharField(
        source='get_priority_display',
        read_only=True
    )
    changeReason_display = serializers.CharField(
        source='get_changeReason_display',
        read_only=True
    )
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'subscriptionId', 'icc', 'userId', 'acctId', 'brand', 'productId',
            'productFlag', 'productFlag_display', 'status', 'status_display',
            'statusTime', 'activeDeadline', 'validityUnit', 'validityUnit_display',
            'validityTime', 'effTime', 'expTime', 'createTime', 'priority',
            'priority_display', 'changeReason', 'changeReason_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_subscriptionId(self, value):
        """验证订阅ID唯一性"""
        if self.instance and self.instance.subscriptionId == value:
            return value
        
        if Subscription.objects.filter(subscriptionId=value).exists():
            raise serializers.ValidationError('订阅ID已存在')
        return value


class SubscriptionListSerializer(serializers.ModelSerializer):
    """
    订阅列表序列化器（简化版）
    """
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    productFlag_display = serializers.CharField(
        source='get_productFlag_display',
        read_only=True
    )
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'subscriptionId', 'userId', 'acctId', 'brand', 'productId',
            'productFlag', 'productFlag_display', 'status', 'status_display',
            'effTime', 'expTime', 'priority', 'created_at'
        ]


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """
    订阅创建序列化器
    """
    class Meta:
        model = Subscription
        fields = [
            'subscriptionId', 'icc', 'userId', 'acctId', 'brand', 'productId',
            'productFlag', 'status', 'statusTime', 'activeDeadline',
            'validityUnit', 'validityTime', 'effTime', 'expTime',
            'createTime', 'priority', 'changeReason'
        ]
    
    def validate_subscriptionId(self, value):
        """验证订阅ID唯一性"""
        if Subscription.objects.filter(subscriptionId=value).exists():
            raise serializers.ValidationError('订阅ID已存在')
        return value


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    """
    订阅更新序列化器
    """
    class Meta:
        model = Subscription
        fields = [
            'icc', 'userId', 'acctId', 'brand', 'productId', 'productFlag',
            'status', 'statusTime', 'activeDeadline', 'validityUnit',
            'validityTime', 'effTime', 'expTime', 'createTime',
            'priority', 'changeReason'
        ]
        # 订阅ID不允许更新
        read_only_fields = ['subscriptionId']
