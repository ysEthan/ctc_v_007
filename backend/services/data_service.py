"""
数据服务层
处理ICC、Subscription、Usage数据的创建和更新
"""
import logging
from typing import Dict, Any, Optional, Tuple
from django.db import transaction
from django.utils import timezone

from apps.ICC.models import ICC
from apps.Subscription.models import Subscription
from apps.Usage.models import Usage
from apps.document.models import BadCase
from .api_clients import api_client_manager

logger = logging.getLogger(__name__)


class DataService:
    """
    数据服务类
    负责处理API响应数据并创建/更新数据库记录
    """
    
    def __init__(self):
        self.api_client = api_client_manager
    
    def process_iccid_data(self, document_id: int, iccid: str) -> Tuple[bool, str]:
        """
        处理单个ICCID的完整数据流程
        
        Args:
            document_id: 文档ID
            iccid: ICCID
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            with transaction.atomic():
                # 1. 获取用户信息
                user_success, user_error = self._process_user_info(document_id, iccid)
                
                # 2. 获取订阅信息
                subscription_success, subscription_error = self._process_subscription_info(document_id, iccid)
                
                # 3. 获取用量信息
                usage_success, usage_error = self._process_usage_info(document_id, iccid)
                
                # 判断整体处理结果
                if user_success and subscription_success and usage_success:
                    return True, "处理成功"
                else:
                    errors = []
                    if not user_success:
                        errors.append(f"用户信息: {user_error}")
                    if not subscription_success:
                        errors.append(f"订阅信息: {subscription_error}")
                    if not usage_success:
                        errors.append(f"用量信息: {usage_error}")
                    
                    return False, "; ".join(errors)
                    
        except Exception as e:
            logger.error(f"处理ICCID {iccid} 时发生异常: {str(e)}")
            return False, f"处理异常: {str(e)}"
    
    def _process_user_info(self, document_id: int, iccid: str) -> Tuple[bool, str]:
        """
        处理用户信息
        
        Args:
            document_id: 文档ID
            iccid: ICCID
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            # 调用API获取用户信息
            result = self.api_client.query_user_info(iccid)
            
            if result.get("code") == "0000":
                user_data = result.get("data", {}).get("user", {})
                if user_data:
                    # 创建或更新ICC记录
                    self._create_or_update_icc(user_data)
                    return True, "成功"
                else:
                    return False, "用户数据为空"
            else:
                # 记录API调用失败
                self._record_bad_case(
                    document_id, iccid, 'user',
                    result.get('_request_info', {}).get('trans_id'),
                    result.get('_request_info', {}).get('status_code'),
                    result, result.get('message', '未知错误')
                )
                return False, result.get('message', 'API调用失败')
                
        except Exception as e:
            logger.error(f"处理用户信息时发生异常: {str(e)}")
            return False, f"异常: {str(e)}"
    
    def _process_subscription_info(self, document_id: int, iccid: str) -> Tuple[bool, str]:
        """
        处理订阅信息
        
        Args:
            document_id: 文档ID
            iccid: ICCID
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            # 调用API获取订阅信息
            result = self.api_client.query_subscription_info(iccid)
            
            if result.get("code") == "0000":
                subscriptions = result.get("data", {}).get("list", [])
                if subscriptions:
                    # 创建或更新订阅记录
                    for sub_data in subscriptions:
                        self._create_or_update_subscription(iccid, sub_data)
                    return True, "成功"
                else:
                    return False, "订阅数据为空"
            else:
                # 记录API调用失败
                self._record_bad_case(
                    document_id, iccid, 'subscription',
                    result.get('_request_info', {}).get('trans_id'),
                    result.get('_request_info', {}).get('status_code'),
                    result, result.get('message', '未知错误')
                )
                return False, result.get('message', 'API调用失败')
                
        except Exception as e:
            logger.error(f"处理订阅信息时发生异常: {str(e)}")
            return False, f"异常: {str(e)}"
    
    def _process_usage_info(self, document_id: int, iccid: str) -> Tuple[bool, str]:
        """
        处理用量信息
        
        Args:
            document_id: 文档ID
            iccid: ICCID
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            # 调用API获取用量信息
            result = self.api_client.query_usage_info(iccid)
            
            if result.get("code") == "0000":
                usages = result.get("data", {}).get("list", [])
                if usages:
                    # 创建或更新用量记录
                    for usage_data in usages:
                        self._create_or_update_usage(iccid, usage_data)
                    return True, "成功"
                else:
                    return False, "用量数据为空"
            else:
                # 记录API调用失败
                self._record_bad_case(
                    document_id, iccid, 'usage',
                    result.get('_request_info', {}).get('trans_id'),
                    result.get('_request_info', {}).get('status_code'),
                    result, result.get('message', '未知错误')
                )
                return False, result.get('message', 'API调用失败')
                
        except Exception as e:
            logger.error(f"处理用量信息时发生异常: {str(e)}")
            return False, f"异常: {str(e)}"
    
    def _create_or_update_icc(self, user_data: Dict[str, Any]) -> ICC:
        """
        创建或更新ICC记录
        
        Args:
            user_data: 用户数据
            
        Returns:
            ICC: ICC实例
        """
        iccid = user_data.get('iccid')
        if not iccid:
            raise ValueError("ICCID不能为空")
        
        # 获取或创建ICC记录
        icc, created = ICC.objects.get_or_create(
            iccid=iccid,
            defaults={
                'userid': user_data.get('userId'),
                'custid': user_data.get('custId'),
                'acctid': user_data.get('acctId'),
                'paidFlag': user_data.get('paidFlag'),
                'imsi': user_data.get('imsi'),
                'msisdn': user_data.get('msisdn'),
                'brand': user_data.get('brand'),
                'rateplanId': user_data.get('rateplanId'),
                'lifeCycle': user_data.get('lifeCycle'),
                'hlrState': user_data.get('hlrState'),
                'lifeCycleTime': user_data.get('lifeCycleTime'),
                'activeType': user_data.get('activeType'),
                'activeTime': user_data.get('activeTime'),
                'effTime': user_data.get('effTime'),
                'expTime': user_data.get('expTime'),
                'createTime': user_data.get('createTime'),
            }
        )
        
        if not created:
            # 更新现有记录
            icc.userid = user_data.get('userId', icc.userid)
            icc.custid = user_data.get('custId', icc.custid)
            icc.acctid = user_data.get('acctId', icc.acctid)
            icc.paidFlag = user_data.get('paidFlag', icc.paidFlag)
            icc.imsi = user_data.get('imsi', icc.imsi)
            icc.msisdn = user_data.get('msisdn', icc.msisdn)
            icc.brand = user_data.get('brand', icc.brand)
            icc.rateplanId = user_data.get('rateplanId', icc.rateplanId)
            icc.lifeCycle = user_data.get('lifeCycle', icc.lifeCycle)
            icc.hlrState = user_data.get('hlrState', icc.hlrState)
            icc.lifeCycleTime = user_data.get('lifeCycleTime', icc.lifeCycleTime)
            icc.activeType = user_data.get('activeType', icc.activeType)
            icc.activeTime = user_data.get('activeTime', icc.activeTime)
            icc.effTime = user_data.get('effTime', icc.effTime)
            icc.expTime = user_data.get('expTime', icc.expTime)
            icc.createTime = user_data.get('createTime', icc.createTime)
            icc.save()
        
        return icc
    
    def _create_or_update_subscription(self, iccid: str, sub_data: Dict[str, Any]) -> Subscription:
        """
        创建或更新订阅记录
        
        Args:
            iccid: ICCID
            sub_data: 订阅数据
            
        Returns:
            Subscription: 订阅实例
        """
        subscription_id = sub_data.get('subscriptionId')
        if not subscription_id:
            raise ValueError("subscriptionId不能为空")
        
        # 获取ICC记录
        try:
            icc = ICC.objects.get(iccid=iccid)
        except ICC.DoesNotExist:
            # 如果ICC不存在，创建一个基本的ICC记录
            icc = ICC.objects.create(
                iccid=iccid,
                # 其他字段留空
            )
        
        # 获取或创建订阅记录
        subscription, created = Subscription.objects.get_or_create(
            subscriptionId=subscription_id,
            defaults={
                'icc': icc,
                'userId': sub_data.get('userId'),
                'acctId': sub_data.get('acctId'),
                'brand': sub_data.get('brand'),
                'productId': sub_data.get('productId'),
                'productFlag': sub_data.get('productFlag'),
                'status': sub_data.get('status'),
                'statusTime': sub_data.get('statusTime'),
                'activeDeadline': sub_data.get('activeDeadline'),
                'validityUnit': sub_data.get('validityUnit'),
                'validityTime': sub_data.get('validityTime'),
                'effTime': sub_data.get('effTime'),
                'expTime': sub_data.get('expTime'),
                'createTime': sub_data.get('createTime'),
                'priority': sub_data.get('priority'),
                'changeReason': sub_data.get('changeReason'),
            }
        )
        
        if not created:
            # 更新现有记录
            subscription.userId = sub_data.get('userId', subscription.userId)
            subscription.acctId = sub_data.get('acctId', subscription.acctId)
            subscription.brand = sub_data.get('brand', subscription.brand)
            subscription.productId = sub_data.get('productId', subscription.productId)
            subscription.productFlag = sub_data.get('productFlag', subscription.productFlag)
            subscription.status = sub_data.get('status', subscription.status)
            subscription.statusTime = sub_data.get('statusTime', subscription.statusTime)
            subscription.activeDeadline = sub_data.get('activeDeadline', subscription.activeDeadline)
            subscription.validityUnit = sub_data.get('validityUnit', subscription.validityUnit)
            subscription.validityTime = sub_data.get('validityTime', subscription.validityTime)
            subscription.effTime = sub_data.get('effTime', subscription.effTime)
            subscription.expTime = sub_data.get('expTime', subscription.expTime)
            subscription.createTime = sub_data.get('createTime', subscription.createTime)
            subscription.priority = sub_data.get('priority', subscription.priority)
            subscription.changeReason = sub_data.get('changeReason', subscription.changeReason)
            subscription.save()
        
        return subscription
    
    def _create_or_update_usage(self, iccid: str, usage_data: Dict[str, Any]) -> Optional[Usage]:
        """
        创建或更新用量记录
        
        Args:
            iccid: ICCID
            usage_data: 用量数据
            
        Returns:
            Usage: 用量实例或None
        """
        try:
            # 获取ICC记录
            icc = ICC.objects.get(iccid=iccid)
            
            # 从用量数据中获取subscriptionId和productId
            subscription_id = usage_data.get('subscriptionId')
            product_id = usage_data.get('productId')
            
            if not subscription_id:
                logger.error(f"用量数据中缺少subscriptionId: {usage_data}")
                return None
            
            # 获取或创建订阅记录
            subscription, created = Subscription.objects.get_or_create(
                subscriptionId=subscription_id,
                defaults={
                    'icc': icc,
                    'productId': product_id or "unknown",
                    'brand': icc.brand,  # 从ICC记录继承
                    'userId': icc.userid,  # 从ICC记录继承
                    'acctId': icc.acctid,  # 从ICC记录继承
                    # 其他字段留空，等待订阅信息API补充
                }
            )
            
            # 如果订阅已存在但productId为空，更新它
            if not created and (not subscription.productId or subscription.productId == "unknown"):
                subscription.productId = product_id or "unknown"
                subscription.save()
            
            # 创建用量记录
            usage = Usage.objects.create(
                usageDate=usage_data.get('usageDate'),
                subscription=subscription,
                subscriptionId=subscription_id,
                productId=product_id or subscription.productId,
                usageType=usage_data.get('usageType', 'dat'),
                callType=usage_data.get('callType'),
                visitMcc=usage_data.get('visitMcc'),
                visitMnc=usage_data.get('visitMnc'),
                usage=usage_data.get('usage'),
                unit=usage_data.get('unit', 'Byte'),
            )
            
            return usage
            
        except ICC.DoesNotExist:
            logger.error(f"ICC记录不存在: {iccid}")
            return None
        except Exception as e:
            logger.error(f"创建用量记录时发生异常: {str(e)}")
            return None
    
    def _record_bad_case(self, document_id: int, iccid: str, api_type: str, 
                        trans_id: str, status_code: int, response_data: Dict[str, Any], 
                        error_message: str):
        """
        记录错误案例
        
        Args:
            document_id: 文档ID
            iccid: ICCID
            api_type: API类型
            trans_id: 事务ID
            status_code: 状态码
            response_data: 响应数据
            error_message: 错误信息
        """
        try:
            from apps.document.models import Document
            document = Document.objects.get(id=document_id)
            
            BadCase.objects.update_or_create(
                document=document,
                iccid=iccid,
                api_type=api_type,
                defaults={
                    'trans_id': trans_id,
                    'status_code': status_code,
                    'response_data': response_data,
                    'error_message': error_message,
                }
            )
        except Exception as e:
            logger.error(f"记录错误案例时发生异常: {str(e)}")


# 全局数据服务实例
data_service = DataService()
